"""Conversations manager."""

from typing import List

from fastapi import APIRouter, Depends, status, Depends
from sqlalchemy.orm.session import Session
from starlette.responses import Response

from app import crud
from app.api.dependencies.database import get_db
from app.api.dependencies.utils import get_limits
from app.schemas.conversation import Conversation, ConversationCreate

router = APIRouter()


@router.post(
    "",
    response_model=Conversation,
    status_code=status.HTTP_201_CREATED,
    summary="Create simple conversation",
)
def conversation_create_post(
    *, db: Session = Depends(get_db), conversation: ConversationCreate
):
    """Creates a new conversation linked to a user."""
    return crud.conversation.create(db, obj_in=conversation)


@router.get(
    "/{conversation_id}",
    response_model=Conversation,
    responses={404: {"description": "Conversation not found"}},
    summary="Get conversation by id",
)
def conversation_get_by_id(*, db: Session = Depends(get_db), conversation_id: int):
    """Finds the conversation by id or returns 404 if it wasn't found."""
    return crud.conversation.get_or_404(db, id=conversation_id)


@router.get(
    "/user/{user_id}",
    response_model=List[Conversation],
    responses={404: {"description": "User not found"}},
    summary="Get conversations from user",
)
def conversation_get_from_user(
    *, db: Session = Depends(get_db), user_id: int, limits: dict = Depends(get_limits)
):
    """Returns a list of conversations linked to a user."""
    crud.user.get_or_404(db, id=user_id)
    return crud.conversation.get_user(db, user_id=user_id, **limits)


@router.get("", response_model=List[Conversation], summary="Get all conversations")
def conversations_get_from_all_users(
    *, db: Session = Depends(get_db), skip: int = 0, limit: int = 100
):
    """Returns a list of all conversations."""
    return crud.conversation.get_multi(db, skip=skip, limit=limit)


@router.delete(
    "/{conversation_id}",
    response_class=Response,
    responses={404: {"description": "Conversation not found"}},
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove a conversation",
)
def conversation_delete(*, db: Session = Depends(get_db), conversation_id: int):
    """Removes a conversation using its id."""
    crud.conversation.remove(db, id=conversation_id)
