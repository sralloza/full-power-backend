from typing import List

from app.security.utils import get_current_user
from fastapi import APIRouter, Depends, HTTPException

from . import crud, schemas

router = APIRouter()


@router.post(
    "/users",
    response_model=schemas.User,
    responses={400: {"description": "Username already registered"}},
)
def users_create_post(user: schemas.UserCreate):
    """Create a new user."""
    if crud.get_user_by_username(username=user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(user=user)


@router.delete("/users", responses={404: {"description": "User not found"}})
def users_delete(user: schemas.UserCreate):
    if not crud.get_user_by_username(username=user.username):
        raise HTTPException(status_code=404, detail="User does not exist")
    return crud.remove_user(user=user)


@router.get("/users", response_model=List[schemas.User])
def users_list_all(skip: int = 0, limit: int = 100):
    """Get all users."""
    users = crud.get_users(skip=skip, limit=limit)
    return users


@router.get("/users/me", response_model=schemas.User)
def users_get_current_user(current_user: schemas.User = Depends(get_current_user)):
    return current_user


@router.get(
    "/users/{user_id}",
    response_model=schemas.User,
    responses={404: {"description": "User not found"}},
)
def users_get_one(user_id: int):
    """Get one user."""
    db_user = crud.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
