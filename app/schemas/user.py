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
    username: Optional[str]
    password: Optional[str]



class UserUpdateAdmin(UserUpdateBasic):
    is_admin: bool = False
    survey_filled: Optional[bool]
    accepted_disclaimer: Optional[bool]

class UserUpdateInner(UserBase):
    username: Optional[str]
    is_admin: Optional[bool]
    hashed_password: Optional[str]
    survey_filled: Optional[bool]
    accepted_disclaimer: Optional[bool]


class UserInDBBase(UserBase):
    is_admin: bool
    survey_filled: bool
    accepted_disclaimer: bool

    class Config:
        orm_mode = True


class UserPublic(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    id: int
    hashed_password: str
    last_login: datetime
