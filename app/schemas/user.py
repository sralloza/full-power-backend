"""Data schematics for user endpoints."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from .conversation import Conversation

# pylint: disable=too-few-public-methods


class UserBase(BaseModel):
    username: str

    def __hash__(self):
        return hash(self.json())


class UserCreateBasic(UserBase):
    password: str


class UserCreateAdmin(UserCreateBasic):
    is_admin: bool = False


class UserCreateAdminInner(UserBase):
    is_admin: bool = False
    hashed_password: str


class UserUpdateBasic(UserBase):
    username: Optional[str] = None
    password: Optional[str] = None


class UserUpdateAdmin(UserUpdateBasic):
    is_admin: bool = False


class UserUpdateInner(UserBase):
    username: Optional[str] = None
    is_admin: Optional[bool] = None
    hashed_password: Optional[str] = None


class UserInDBBase(UserBase):
    id: int
    is_admin: bool

    class Config:
        orm_mode = True


class UserInDB(UserInDBBase):
    hashed_password: str
    last_login: datetime
    conversations: List[Conversation]


class User(UserInDBBase):
    pass
