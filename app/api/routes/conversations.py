"""Conversations manager."""

from typing import List

from fastapi import APIRouter

from . import schemas
from app import crud
from .crud import (
    create_conversation,
    list_all_conversations,
    list_user_conversations,
    remove_conversation,
)

router = APIRouter()


@router.post("/user/{user_id}", response_model=schemas.Conversation)
def conversation_create_post(user_id: int, conversation: schemas.ConversationCreate):
    """Creates a new conversation linked to a user."""

    return create_conversation(conversation=conversation, user_id=user_id)


@router.get("/user/{user_id}", response_model=List[schemas.Conversation])
def conversation_get_from_user(user_id: int, skip: int = 0, limit: int = 100):
    """Returns a list of conversations linked to a user."""

    return list_user_conversations(user_id=user_id, skip=skip, limit=limit)


@router.get("/", response_model=List[schemas.Conversation])
def conversations_get_from_all_users(skip: int = 0, limit: int = 100):
    """Returns a list of all conversations."""

    return list_all_conversations(skip=skip, limit=limit)


@router.delete(
    "/{conversation_id}/", responses={404: {"description": "Conversation not found"}}
)
def conversation_delete(conversation_id: int):
    """Removes a conversation."""

    return remove_conversation(conversation_id)
