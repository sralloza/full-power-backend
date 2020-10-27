"""Routes for managing users (most of them require admin access, except /me)."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm.session import Session

from app import crud
from app.api.dependencies.database import get_db
from app.api.dependencies.security import get_current_user
from app.schemas.user import User, UserCreateAdmin

router = APIRouter()


@router.post(
    "/",
    response_model=User,
    responses={400: {"description": "Username already registered"}},
    dependencies=[Security(get_current_user, scopes=["admin"])],
)
def users_create_post(*, db: Session = Depends(get_db), user: UserCreateAdmin):
    """Creates a new user (can be admin, unlike in /register)."""

    return crud.user.create(db, obj_in=user)


@router.get(
    "/",
    response_model=List[User],
    dependencies=[Security(get_current_user, scopes=["admin"])],
)
def users_list_all(*, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """Returns all users."""

    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.get("/me", response_model=User)
def users_get_current_user(
    current_user: User = Depends(get_current_user),
):
    """Returns the current user."""

    return current_user


@router.get(
    "/{user_id}",
    response_model=User,
    dependencies=[Security(get_current_user, scopes=["admin"])],
    responses={404: {"description": "User not found"}},
)
def users_get_one(*, db: Session = Depends(get_db), user_id: int):
    """Returns a user by its id."""

    db_user = crud.user.get(db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete(
    "/{user_id}",
    responses={404: {"description": "User not found"}},
    dependencies=[Security(get_current_user, scopes=["admin"])],
)
def users_delete(*, db: Session = Depends(get_db), user_id: int):
    """Deletes a user."""

    if not crud.user.get(db, id=user_id):
        raise HTTPException(status_code=404, detail="User does not exist")
    return crud.user.remove(db, id=user_id)
