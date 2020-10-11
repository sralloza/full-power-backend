from typing import List

from fastapi import APIRouter

from . import schemas
from .crud import create_conversation, list_all_conversations, list_user_conversations

router = APIRouter()


@router.post("/conversations/user/{user_id}", response_model=schemas.Conversation)
def conversation_post_one(user_id: int, conversation: schemas.ConversationCreate):
    return create_conversation(conversation=conversation, user_id=user_id)


@router.get("/conversations/user/{user_id}", response_model=List[schemas.Conversation])
def conversation_get_one(user_id: int, skip: int = 0, limit: int = 100):
    return list_user_conversations(user_id=user_id, skip=skip, limit=limit)


@router.get("/conversations", response_model=List[schemas.Conversation])
def conversations_get_all(skip: int = 0, limit: int = 100):
    return list_all_conversations(skip=skip, limit=limit)
