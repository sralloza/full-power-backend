"""Routes for managing users (most of them require admin access, except /me)."""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from starlette.responses import Response

from app import crud
from app.api.dependencies.database import get_db
from app.api.dependencies.utils import get_limits
from app.schemas.user import User, UserCreateAdmin

router = APIRouter()


@router.post(
    "",
    response_model=User,
    responses={409: {"description": "Username already registered"}},
    status_code=201,
    summary="Create new user",
)
def users_create_post(*, db: Session = Depends(get_db), user: UserCreateAdmin):
    """Creates a new user (can be admin, unlike in /register)."""
    return crud.user.create(db, obj_in=user)


@router.get(
    "",
    response_model=List[User],
    responses={409: {"description": "Username already registered"}},
    summary="List all users",
)
def users_list_all(
    *, db: Session = Depends(get_db), limits: dict = Depends(get_limits)
):
    """Returns all users."""

    users = crud.user.get_multi(db, **limits)
    return users


@router.get(
    "/{user_id}",
    response_model=User,
    responses={404: {"description": "User not found"}},
    summary="Get user by id",
)
def users_get_one(*, db: Session = Depends(get_db), user_id: int):
    """Returns a user by its id."""

    return crud.user.get_or_404(db, id=user_id)


@router.delete(
    "/{user_id}",
    response_class=Response,
    responses={404: {"description": "User not found"}},
    status_code=204,
    summary="Delete user",
)
def users_delete(*, db: Session = Depends(get_db), user_id: int):
    """Deletes a user."""

    crud.user.remove(db, id=user_id)
