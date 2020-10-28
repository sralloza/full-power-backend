"""Manages database connections involving users."""
import logging

from fastapi import HTTPException
from sqlalchemy.orm.session import Session

from app.core.security import get_password_hash
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreateAdmin, UserUpdate

logger = logging.getLogger(__name__)


class CRUDUser(CRUDBase[User, UserCreateAdmin, UserUpdate]):
    def create(self, db: Session, *, obj_in: UserCreateAdmin) -> User:
        obj_dict = obj_in.dict()
        obj_dict["hashed_password"] = get_password_hash(obj_dict.pop("password"))
        db_obj = User(**obj_dict)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_username(self, db: Session, *, username: str) -> User:
        """Returns a user given its username."""

        return db.query(self.model).filter_by(username=username).first()


user = CRUDUser(User)
