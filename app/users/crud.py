"""Manages database connections involving users."""
import logging

from fastapi import HTTPException

from app.database import db, models
from app.security.utils import get_password_hash

from . import schemas


logger = logging.getLogger(__name__)


def get_user(user_id: int):
    """Returns a user given its id."""

    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(username: str) -> models.User:
    """Returns a user given its username."""

    return db.query(models.User).filter(models.User.username == username).first()


def get_users(skip: int = 0, limit: int = 100):
    """Returns all the users."""

    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(user: schemas.UserCreate):
    """Creates a new user in the database."""

    if get_user_by_username(username=user.username):
        logger.warning(
            "Can't register user with username=%s as it's already registered", user.username
        )
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username, hashed_password=hashed_password, is_admin=user.is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    logger.info("Registered user with username=%r and id=%d", user.username, user.id)
    return db_user


def remove_user(user_id: int):
    """Removes a user."""

    db_user = get_user(user_id=user_id)

    if not db_user:
        logger.warning("Can't remove user with id=%d as it doesn't exist", user_id)
        raise HTTPException(404, "User not found")

    for conversation in db_user.conversations:
        db.delete(conversation)

    db.delete(db_user)
    db.commit()

    logger.debug("Removed user with id=%d", db_user.id)

def create_sample_user():
    """Creates a sample admin user (used in development only)."""

    user = schemas.UserCreate(username="admin", password="1234", is_admin=True)
    return create_user(user)
