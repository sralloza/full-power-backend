from typing import Optional
from pydantic import BaseModel, Field


class UserInput(BaseModel):
    user_msg: str = Field(..., example="Hi bot! What time is it?")


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
