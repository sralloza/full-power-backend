"""Routes for managing users (most of them require admin access, except /me)."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Security

from app.security.utils import get_current_user

from . import crud, schemas

router = APIRouter()


@router.post(
    "/",
    response_model=schemas.PrivateUser,
    responses={400: {"description": "Username already registered"}},
    dependencies=[Security(get_current_user, scopes=["admin"])],
)
def users_create_post(user: schemas.UserCreate):
    """Creates a new user (can be admin, unlike in /register)."""

    return crud.create_user(user=user)


@router.delete(
    "/{user_id}",
    responses={404: {"description": "User not found"}},
    dependencies=[Security(get_current_user, scopes=["admin"])],
)
def users_delete(user_id: int):
    """Deletes a user."""

    if not crud.get_user(user_id=user_id):
        raise HTTPException(status_code=404, detail="User does not exist")
    return crud.remove_user(user_id=user_id)


@router.get(
    "/",
    response_model=List[schemas.PrivateUser],
    dependencies=[Security(get_current_user, scopes=["admin"])],
)
def users_list_all(skip: int = 0, limit: int = 100):
    """Returns all users."""

    users = crud.get_users(skip=skip, limit=limit)
    return users


@router.get(
    "/{user_id}",
    response_model=schemas.PrivateUser,
    dependencies=[Security(get_current_user, scopes=["admin"])],
    responses={404: {"description": "User not found"}},
)
def users_get_one(user_id: int):
    """Returns a user by its id."""

    db_user = crud.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/me", response_model=schemas.PrivateUser)
def users_get_current_user(
    current_user: schemas.PrivateUser = Depends(get_current_user),
):
    """Returns the current user."""

    return current_user
