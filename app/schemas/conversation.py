"""Data schematics for conversation endpoints."""


from typing import Optional
from pydantic import BaseModel

# pylint: disable=too-few-public-methods


class ConversationBase(BaseModel):
    """Base class for conversations data."""

    user_msg: str
    bot_msg: str
    intent: str
    user_id: int


class ConversationCreate(ConversationBase):
    pass


class ConversationUpdate(BaseModel):
    user_msg: Optional[str]
    bot_msg: Optional[str]
    intent: Optional[str]
    user_id: Optional[int]


class ConversationInDB(ConversationBase):
    id: int

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True


class Conversation(ConversationInDB):
    pass
