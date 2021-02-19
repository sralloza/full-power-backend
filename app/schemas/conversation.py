"""Data schematics for conversation endpoints."""


from enum import Enum
from typing import List, Optional

from pydantic import BaseModel
from pydantic.class_validators import validator

from app.utils.bot import split_bot_msg

# pylint: disable=too-few-public-methods


class DisplayType(Enum):
    default = "default"
    five_stars = "five_stars"
    yes_no = "yes_no"


class ConversationBase(BaseModel):
    """Base class for conversations data."""

    user_msg: str
    bot_msg: str
    intent: str
    user_id: int


class ConversationCreate(ConversationBase):
    pass


class ConversationOut(ConversationCreate):
    display_type: DisplayType
    bot_msg: List[str]

    @validator("bot_msg", pre=True)
    def split_bot_response(cls, v):
        if isinstance(v, str):
            return split_bot_msg(v)
        return v

    class Config:
        orm_mode = True


class ConversationCreateResult(ConversationCreate):
    display_type: DisplayType

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True


class ConversationCreateInner(ConversationCreateResult):
    pass


class ConversationUpdate(ConversationBase):
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
