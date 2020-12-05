from typing import Generator

from sqlalchemy.orm.session import Session

from app.core.images import process_image_content
from app.models.image import Image
from app.schemas.image import ImageCreate, ImageCreateInner, ImageUpdate

from .base import CRUDBase

IDGenerator = Generator[int, None, None]


class CRUDImage(CRUDBase[Image, ImageCreateInner, ImageUpdate]):
    def get_id_list(self, db: Session, *, skip=0, limit=100) -> IDGenerator:
        for line in db.query(self.model.id).offset(skip).limit(limit).all():
            yield line[0]

    def create(self, db: Session, *, obj_in: ImageCreate) -> Image:
        real_image = process_image_content(obj_in.content)
        return super().create(db, obj_in=real_image)

    def update(self, db: Session, *, db_obj: Image, obj_in: ImageUpdate) -> Image:
        if obj_in.content:
            obj_in = ImageUpdate(**process_image_content(obj_in.content).dict())
        return super().update(db, db_obj=db_obj, obj_in=obj_in)


image = CRUDImage(Image)
