"""Image related routes."""

from typing import List

from fastapi import APIRouter, Depends, File, Response, Security
from sqlalchemy.orm.session import Session

from app import crud
from app.api.dependencies.database import get_db
from app.api.dependencies.security import get_current_user
from app.schemas.image import ImageCreate, ImageCreateResult

router = APIRouter()


@router.get(
    "/{image_id}",
    responses={404: {"description": "Image not found"}},
    summary="Get image by id",
)
def get_image(*, db: Session = Depends(get_db), image_id: int):
    """Finds the image by its id or returns 404."""
    image = crud.image.get_or_404(db, id=image_id)
    return Response(content=image.content, media_type=image.mime_type)


@router.get("", response_model=List[int], summary="List image ids")
def get_image_id_list(*, db: Session = Depends(get_db), skip=0, limit=100):
    """List image ids."""
    return crud.image.get_id_list(db, skip=skip, limit=limit)


@router.post(
    "",
    dependencies=[Security(get_current_user, scopes=["admin"])],
    response_model=ImageCreateResult,
    responses={415: {"description": "Image type or mime type could not be identified"}},
    status_code=201,
    summary="Create image",
)
def create_image(*, db: Session = Depends(get_db), image_content: bytes = File(...)):
    """Creates an image."""
    image = ImageCreate(content=image_content)
    return crud.image.create(db, obj_in=image)


@router.delete(
    "/multiple",
    dependencies=[Security(get_current_user, scopes=["admin"])],
    response_class=Response,
    status_code=204,
    summary="Remove multiple images",
)
def remove_image_list(*, db: Session = Depends(get_db), ids: List[int]):
    """Removes a bulk of images using their ids."""
    for image_id in ids:
        crud.image.remove(db, id=image_id)


@router.delete(
    "/{image_id}",
    dependencies=[Security(get_current_user, scopes=["admin"])],
    response_class=Response,
    status_code=204,
    summary="Remove one image",
)
def remove_image(*, db: Session = Depends(get_db), image_id: int):
    """Removes an image using its id."""
    crud.image.remove(db, id=image_id)
