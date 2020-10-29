"""Data schematics for user endpoints."""

from typing import List, Optional

from pydantic import BaseModel, validator

from .conversation import Conversation

# pylint: disable=too-few-public-methods


class UserBase(BaseModel):
    username: str


class UserCreateBasic(BaseModel):
    password: str


class UserCreateAdmin(UserCreateBasic):
    is_admin: bool = False


class UserUpdateBasic(UserBase):
    username: Optional[str] = None
    password: Optional[str] = None

    @validator("*", pre=True, always=True)
    def at_least_one_value(cls, value, values, **kwargs):
        if not values and value is None:
            raise ValueError("At least one field is required")
        return value


class UserUpdateAdmin(UserUpdateBasic):
    is_admin: bool = False


class UserInDB(BaseModel):
    is_admin: bool

    id: int
    conversations: List[Conversation] = []
    hashed_password: str

    class Config:
        orm_mode = True


class User(UserInDB):
    username: str
    is_admin: str

    class Config:
        orm_mode = True
