"""Routes for managing users (most of them require admin access, except /me)."""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from app import crud
from app.api.dependencies.database import get_db
from app.core.users import raise_user_already_registered, raise_user_not_found
from app.schemas.user import User, UserCreateAdmin

router = APIRouter()


@router.post(
    "",
    response_model=User,
    responses={400: {"description": "Username already registered"}},
)
def users_create_post(*, db: Session = Depends(get_db), user: UserCreateAdmin):
    """Creates a new user (can be admin, unlike in /register)."""
    if crud.user.get_by_username(db, username=user.username):
        raise_user_already_registered()

    return crud.user.create(db, obj_in=user)


@router.get("", response_model=List[User])
def users_list_all(*, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """Returns all users."""

    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.get(
    "/{user_id}",
    response_model=User,
    responses={404: {"description": "User not found"}},
)
def users_get_one(*, db: Session = Depends(get_db), user_id: int):
    """Returns a user by its id."""

    db_user = crud.user.get(db, id=user_id)
    if db_user is None:
        raise_user_not_found()
    return db_user


@router.delete(
    "/{user_id}", responses={404: {"description": "User not found"}}, status_code=204
)
def users_delete(*, db: Session = Depends(get_db), user_id: int):
    """Deletes a user."""

    if not crud.user.get(db, id=user_id):
        raise_user_not_found()
    return crud.user.remove(db, id=user_id)
