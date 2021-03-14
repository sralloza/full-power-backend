import logging
import re
from typing import Generator, Optional

from fastapi import HTTPException
from sqlalchemy.orm.session import Session

from app.core.files import get_file_id_from_name
from app.models.file import File
from app.schemas.file import (
    FileCreate,
    FileCreateInner,
    FileCreateResult,
    FileUpdate,
    FileUpdateInner,
)

from .base import CRUDBase

logger = logging.getLogger(__name__)
NameGenerator = Generator[FileCreateResult, None, None]
IMAGE_PATTERN = re.compile(r"<img src=\"https?:\/\/[\w.]+\/images\/(\d+)\">")


class CRUDFile(CRUDBase[File, FileCreate, FileUpdateInner]):
    def get_by_name(self, db: Session, name: str, lang: str) -> Optional[File]:
        file_id = get_file_id_from_name(name, lang)
        return super().get(db, id=file_id)

    def create(self, db: Session, *, obj_in: FileCreateInner) -> File:
        try:
            return super().create(db, obj_in=obj_in)
        except HTTPException as exc:
            name = obj_in.name
            lang = obj_in.lang
            detail = f"File with name={name} and lang={lang} already exists"
            raise HTTPException(409, detail) from exc

    def update(self, db: Session, *, db_obj: File, obj_in: FileUpdate) -> File:
        update_dict = obj_in.dict(exclude_unset=True)
        name_supplied = update_dict.get("name", None)
        lang_supplied = update_dict.get("lang", None)

        update = name_supplied is not None or lang_supplied is not None

        if update:
            lang = lang_supplied or db_obj.lang
            name = name_supplied or db_obj.name
            update_dict["id"] = get_file_id_from_name(name, lang)

        new_file = super().update(
            db, db_obj=db_obj, obj_in=FileUpdateInner(**update_dict)
        )
        self.autoremove_images(db)
        return new_file

    def get_or_404_by_name(self, db: Session, name: str, lang: str) -> File:
        file_id = get_file_id_from_name(name, lang)
        try:
            return super().get_or_404(db, id=file_id)
        except HTTPException as exc:
            detail = f"File with name={name} and lang={lang} does not exist"
            raise HTTPException(404, detail) from exc

    def remove_by_name(self, db: Session, *, name: str, lang: str) -> None:
        obj = self.get_or_404_by_name(db, name=name, lang=lang)
        return self.remove(db, id=obj.id)

    def remove(self, db: Session, *, id: str):
        super().remove(db, id=id)
        self.autoremove_images(db)

    def get_db_file_list(
        self, db: Session, *, lang: str, skip: int = 0, limit: int = 100
    ) -> NameGenerator:
        attrs = (self.model.name, self.model.title, self.model.lang)
        query = db.query(*attrs).filter_by(lang=lang)
        query = query.order_by(self.model.name.asc()).offset(skip).limit(limit)
        for line in query.all():
            yield FileCreateResult(name=line[0], title=line[1], lang=line[2])

    def autoremove_images(self, db: Session):
        from app import crud

        used_images = set()

        for file in self.get_multi(db, limit=10000):
            used_images |= {
                int(x.group(1)) for x in IMAGE_PATTERN.finditer(file.content)
            }

        existing_images = set(crud.image.get_id_list(db, limit=10000))
        images_to_remove = existing_images - used_images
        logger.info("Automatically removing useless images: %r", images_to_remove)

        for image_id in images_to_remove:
            crud.image.remove(db, id=image_id)


file = CRUDFile(File)
