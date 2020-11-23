"""Conversations manager."""

from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from starlette.responses import Response

from app import crud
from app.api.dependencies.database import get_db
from app.schemas.conversation import Conversation, ConversationCreate

router = APIRouter()


@router.post("", response_model=Conversation)
def conversation_create_post(
    *, db: Session = Depends(get_db), conversation: ConversationCreate
):
    """Creates a new conversation linked to a user."""

    return crud.conversation.create(db, obj_in=conversation)


@router.get("/user/{user_id}", response_model=List[Conversation])
def conversation_get_from_user(
    *, db: Session = Depends(get_db), user_id: int, skip: int = 0, limit: int = 100
):
    """Returns a list of conversations linked to a user."""

    return crud.conversation.get_user(db, user_id=user_id, skip=skip, limit=limit)


@router.get("", response_model=List[Conversation])
def conversations_get_from_all_users(
    *, db: Session = Depends(get_db), skip: int = 0, limit: int = 100
):
    """Returns a list of all conversations."""

    return crud.conversation.get_multi(db, skip=skip, limit=limit)


@router.delete(
    "/{conversation_id}",
    responses={404: {"description": "Conversation not found"}},
    status_code=204,
)
def conversation_delete(*, db: Session = Depends(get_db), conversation_id: int):
    """Removes a conversation."""

    crud.conversation.remove(db, id=conversation_id)
    return Response(status_code=HTTPStatus.NO_CONTENT.value)
