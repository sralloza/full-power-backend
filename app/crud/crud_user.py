"""Manages database connections involving users."""
import logging
from typing import Union

from fastapi import HTTPException
from sqlalchemy.orm.session import Session

from app.core.security import get_password_hash
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import (
    UserCreateAdmin,
    UserCreateAdminInner,
    UserUpdateAdmin,
    UserUpdateBasic,
    UserUpdateInner,
)

logger = logging.getLogger(__name__)
UserUpdateAlias = Union[UserUpdateAdmin, UserUpdateBasic]


class CRUDUser(CRUDBase[User, UserCreateAdminInner, UserUpdateInner]):
    def create(self, db: Session, *, obj_in: UserCreateAdmin) -> User:
        if self.get_by_username(db, username=obj_in.username):
            raise HTTPException(400, f"User {obj_in.username!r} is already registered")

        obj_dict = obj_in.dict()
        obj_dict["hashed_password"] = get_password_hash(obj_dict.pop("password"))
        return super().create(db, obj_in=UserCreateAdminInner(**obj_dict))

    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdateAlias) -> User:
        obj_dict = obj_in.dict(exclude_unset=True)
        if "username" in obj_dict:
            if self.get_by_username(db, username=obj_dict["username"]):
                raise HTTPException(
                    400, f"User {obj_in.username!r} is already registered"
                )

        if "password" in obj_dict:
            obj_dict["hashed_password"] = get_password_hash(obj_dict.pop("password"))

        return super().update(db, db_obj=db_obj, obj_in=UserUpdateInner(**obj_dict))

    def get_by_username(self, db: Session, *, username: str) -> User:
        """Returns a user given its username."""

        return db.query(self.model).filter_by(username=username).first()


user = CRUDUser(User)
