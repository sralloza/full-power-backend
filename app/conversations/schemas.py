from typing import Optional

from app.bot.schemas import UserInput
from pydantic import Field


class BaseConversation(UserInput):
    bot_msg: str = Field(..., example="Hi! It's 20:30.")
    intent: Optional[str]


class Conversation(BaseConversation):
    user_id: int
    id: int

    class Config:
        orm_mode = True


class ConversationCreate(BaseConversation):
    pass
