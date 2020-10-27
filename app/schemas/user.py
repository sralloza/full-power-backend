"""Data schematics for user endpoints."""

from typing import List

from pydantic import BaseModel

from .conversation import Conversation

# pylint: disable=too-few-public-methods


class UserBase(BaseModel):
    """Shared properties."""

    username: str


class PlainPasswordMixin(BaseModel):
    password: str


class IdMixin(BaseModel):
    id: int


class AdminMixin(BaseModel):
    is_admin: bool


class UserCreateBasic(UserBase, PlainPasswordMixin):
    pass


class UserCreateAdmin(UserCreateBasic, AdminMixin):
    pass


class UserUpdate(UserCreateBasic):
    pass


class UserInDBBase(UserBase, IdMixin, AdminMixin):
    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    conversations: List[Conversation] = []
    hashed_password: str
