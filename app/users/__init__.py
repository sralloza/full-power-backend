from typing import List

from fastapi import APIRouter, HTTPException

from . import crud, schemas

router = APIRouter()


@router.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate):
    """Create a new user."""
    if crud.get_user_by_username(username=user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(user=user)


@router.delete("/users")
def remove_user(user: schemas.UserCreate):
    if not crud.get_user_by_username(username=user.username):
        raise HTTPException(status_code=404, detail="User does not exist")
    return crud.remove_user(user=user)


@router.get("/users", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100):
    """Get all users."""
    users = crud.get_users(skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int):
    """Get one user."""
    db_user = crud.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
