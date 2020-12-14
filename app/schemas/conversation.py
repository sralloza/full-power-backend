"""Data schematics for conversation endpoints."""


from enum import Enum
from typing import Optional

from pydantic import BaseModel

# pylint: disable=too-few-public-methods


class DisplayType(Enum):
    default = "default"
    five_stars = "five_stars"


class ConversationBase(BaseModel):
    """Base class for conversations data."""

    user_msg: str
    bot_msg: str
    intent: str
    user_id: int


class ConversationCreate(ConversationBase):
    pass


class ConversationCreateResult(ConversationCreate):
    display_type: DisplayType

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True


class ConversationCreateInner(ConversationCreateResult):
    pass


class ConversationUpdate(BaseModel):
    user_msg: Optional[str]
    bot_msg: Optional[str]
    intent: Optional[str]
    user_id: Optional[int]


class ConversationInDB(ConversationBase):
    display_type: DisplayType
    id: int

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True


class Conversation(ConversationInDB):
    pass
