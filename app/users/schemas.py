"""Data schematics for user endpoints."""

from typing import List

from pydantic import BaseModel

# pylint: disable=too-few-public-methods


class ConversationBase(BaseModel):
    """Base model for conversations."""

    user_msg: str
    bot_msg: str


class ConversationCreate(ConversationBase):
    """Model for creating conversations."""


class Conversation(ConversationBase):
    """"Model for conversations stored in database."""

    id: int
    user_id: int

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True


class UserBase(BaseModel):
    """Base models for users."""

    username: str


class BasicUserCreate(UserBase):
    """Model for creating basic users."""

    password: str


class UserCreate(BasicUserCreate):
    """User's data ready to send to the database."""

    is_admin: bool


class UserPublic(UserBase):
    """User's public data."""

    hashed_password: str

    class Config: # pylint: disable=missing-class-docstring
        orm_mode = True


class PrivateUser(UserPublic):
    """Model for manage all the user's data, even the private data."""

    id: int
    conversations: List[Conversation] = []
