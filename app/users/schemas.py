from typing import List

from pydantic import BaseModel


class ConversationBase(BaseModel):
    """Base model for conversations."""

    user_msg: str
    bot_msg: str


class ConversationCreate(ConversationBase):
    """Model for creating conversations."""

    pass


class Conversation(ConversationBase):
    """"Model for conversations stored in database."""

    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    """Base models for users."""

    username: str


class BasicUserCreate(UserBase):
    """Model for creating basic users."""

    password: str


class UserCreate(BasicUserCreate):
    is_admin: bool


class UserPublic(UserBase):
    hashed_password: str

    class Config:
        orm_mode = True


class User(UserPublic):
    id: int
    conversations: List[Conversation] = []
