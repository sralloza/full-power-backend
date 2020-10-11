from typing import List

from pydantic import BaseModel


class ConversationBase(BaseModel):
    user_msg: str
    bot_msg: str


class ConversationCreate(ConversationBase):
    pass


class Conversation(ConversationBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    is_admin: bool


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    hashed_password: str
    conversations: List[Conversation] = []

    class Config:
        orm_mode = True
