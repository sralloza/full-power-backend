"""Data schematics for user endpoints."""

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


class UserUpdateBasic(UserBase):
    username: Optional[str] = None
    password: Optional[str] = None


class UserUpdateAdmin(UserUpdateBasic):
    is_admin: bool = False


class UserInDB(UserBase):
    is_admin: bool

    id: int
    conversations: List[Conversation] = []
    hashed_password: str

    class Config:
        orm_mode = True


class User(UserInDB):
    class Config:
        orm_mode = True
