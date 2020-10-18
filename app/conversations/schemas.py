"""Data schematics for conversation endpoints."""

from typing import Optional

from pydantic import Field

from app.bot.schemas import UserInput

# pylint: disable=too-few-public-methods


class BaseConversation(UserInput):
    """Base class for conversations data."""

    bot_msg: str = Field(..., example="Hi! It's 20:30.")
    intent: Optional[str]


class Conversation(BaseConversation):
    """Represents a conversation stored in the database."""

    user_id: int
    id: int

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True


class ConversationCreate(BaseConversation):
    """Represents the data needed to create a conversation."""
