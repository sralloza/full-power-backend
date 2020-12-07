"""File related routes."""

from typing import List

from fastapi import APIRouter, Depends
from fastapi.param_functions import Security
from sqlalchemy.orm.session import Session
from starlette.responses import Response

from app import crud
from app.api.dependencies.database import get_db
from app.api.dependencies.security import get_current_user
from app.core.files import get_file_id_from_name
from app.schemas.file import (
    FileCreate,
    FileCreateInner,
    FileCreateResult,
    FileDelete,
    FileUpdate,
    FileResult,
)

router = APIRouter()


@router.get(
    "",
    response_model=List[FileCreateResult],
    summary="List file names for language in the database",
)
def list_files(
    *, db: Session = Depends(get_db), lang: str = "en", skip: int = 0, limit: int = 100
):
    """Returns a list of the names written in a specific language."""
    return crud.file.get_db_file_list(db, lang=lang, skip=skip, limit=limit)


@router.get(
    "/{name}",
    response_model=FileResult,
    responses={404: {"description": "File not found"}},
    summary="Get file by name and language",
)
def get_file_by_name(*, db: Session = Depends(get_db), name: str, lang: str = "en"):
    """Finds a file by name and language or returns 404 if it can't find it."""
    return crud.file.get_or_404_by_name(db, name=name, lang=lang)


@router.post(
    "",
    response_model=FileCreateResult,
    dependencies=[Security(get_current_user, scopes=["admin"])],
    summary="Create new file",
)
def create_file(*, db: Session = Depends(get_db), file: FileCreate, lang: str = "en"):
    """Creates a new file"""
    file_id = get_file_id_from_name(file.name, lang)
    real_file = FileCreateInner(id=file_id, lang=lang, **file.dict())
    return crud.file.create(db, obj_in=real_file)


@router.put(
    "/{name}",
    response_model=FileCreateResult,
    dependencies=[Security(get_current_user, scopes=["admin"])],
    summary="Update the contents of a file",
)
def update_file(
    *, db: Session = Depends(get_db), name: str, file: FileUpdate, lang: str = "en"
):
    """Update the contents of a file."""
    file_db = crud.file.get_or_404_by_name(db, name=name, lang=lang)
    return crud.file.update(db, db_obj=file_db, obj_in=file)


@router.delete(
    "/multiple",
    dependencies=[Security(get_current_user, scopes=["admin"])],
    response_class=Response,
    status_code=204,
    summary="Remove multiple files",
)
def remove_file_list(*, db: Session = Depends(get_db), files: List[FileDelete]):
    """Removes a bulk of files using their names and language."""
    for file in files:
        crud.file.remove_by_name(db, name=file.name, lang=file.lang)


@router.delete(
    "/{name}",
    status_code=204,
    response_class=Response,
    dependencies=[Security(get_current_user, scopes=["admin"])],
    summary="Remove a file",
)
def remove_file(*, db: Session = Depends(get_db), name: str, lang: str = "en"):
    """Remove a file given its name and language."""
    crud.file.remove_by_name(db, name=name, lang=lang)
