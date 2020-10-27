"""Manages database connections involving users."""
import logging

from fastapi import HTTPException
from sqlalchemy.orm.session import Session
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


logger = logging.getLogger(__name__)


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_username(self, db: Session, *, username: str) -> User:
        """Returns a user given its username."""

        return db.query(self.model).filter_by(username=username).first()


user = CRUDUser(User)
