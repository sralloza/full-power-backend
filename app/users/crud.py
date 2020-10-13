from app.database import db, models
from app.security.utils import get_password_hash
from fastapi import HTTPException

from . import schemas


def get_user(user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(user: schemas.UserCreate):
    if get_user_by_username(username=user.username):
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username, hashed_password=hashed_password, is_admin=user.is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def remove_user(user: schemas.UserCreate):
    db_user = get_user_by_username(user.username)
    db.delete(db_user)
    db.commit()
    return


def _sample_user():
    user = schemas.UserCreate(username="admin", password="1234", is_admin=True)
    return create_user(user)
