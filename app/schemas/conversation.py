"""Data schematics for conversation endpoints."""

from typing import Optional

from pydantic import BaseModel

from .user import UserInput

# pylint: disable=too-few-public-methods


class ConversationBase(BaseModel):
    """Base class for conversations data."""

    user_msg: str
    bot_msg: str
    intent: str
    user_id: int


class ConversationCreate(ConversationBase):
    pass


# Just for CRUD compatibility, conversations can't be updated
class ConversationUpdate(BaseModel):
    pass


class ConversationInDB(ConversationBase):
    id: int

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True

class Conversation(ConversationInDB):
    pass
