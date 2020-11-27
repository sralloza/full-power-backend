"""Manages database connections involving users."""
import logging
from typing import Union

from sqlalchemy.orm.session import Session

from app.core.security import get_password_hash
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import (
    UserCreateAdmin,
    UserCreateAdminDBIn,
    UserUpdateAdmin,
    UserUpdateBasic,
)

logger = logging.getLogger(__name__)
UserUpdateAlias = Union[UserUpdateAdmin, UserUpdateBasic]


class CRUDUser(CRUDBase[User, UserCreateAdminDBIn, UserUpdateAdmin]):
    def create(self, db: Session, *, obj_in: UserCreateAdmin) -> User:
        obj_dict = obj_in.dict()
        obj_dict["hashed_password"] = get_password_hash(obj_dict.pop("password"))
        return super().create(db, obj_in=UserCreateAdminDBIn(**obj_dict))

    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdateAlias) -> User:
        obj_dict = obj_in.dict()
        obj_dict["hashed_password"] = get_password_hash(obj_dict.pop("password"))
        return super().update(db, db_obj=db_obj, obj_in=obj_dict)

    def get_by_username(self, db: Session, *, username: str) -> User:
        """Returns a user given its username."""

        return db.query(self.model).filter_by(username=username).first()


user = CRUDUser(User)
