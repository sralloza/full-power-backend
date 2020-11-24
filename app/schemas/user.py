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


class UserInDBBase(UserBase):
    id: int
    is_admin: bool

    class Config:
        orm_mode = True


class UserInDB(UserInDBBase):
    hashed_password: str
    conversations: List[Conversation] = []


class User(UserInDBBase):
    class Config:
        orm_mode = True
