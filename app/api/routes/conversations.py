"""Conversations manager."""

from typing import List

from fastapi import APIRouter, Depends, Security, status
from sqlalchemy.orm.session import Session
from starlette.responses import Response

from app import crud
from app.api.dependencies.database import get_db
from app.api.dependencies.security import get_current_user
from app.api.dependencies.utils import get_limits
from app.schemas.conversation import Conversation, ConversationCreate
from app.utils.responses import gen_responses

router = APIRouter(
    dependencies=[Security(get_current_user, scopes=["admin"])],
    prefix="/conversations",
    tags=["Conversations"],
    **gen_responses({403: "Admin access required"}),
)


@router.post(
    "",
    response_description="The created transcripted conversation",
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
    response_description="The transcripted conversation",
    response_model=Conversation,
    summary="Get conversation by id",
    **gen_responses({404: "Conversation not found"}),
)
def conversation_get_by_id(*, db: Session = Depends(get_db), conversation_id: int):
    """Finds the conversation by id or returns 404 if it wasn't found."""
    return crud.conversation.get_or_404(db, id=conversation_id)


@router.get(
    "/user/{user_id}",
    response_description="The user's transcripted conversations",
    response_model=List[Conversation],
    summary="Get conversations from user",
    **gen_responses({404: "User not found"}),
)
def conversation_get_from_user(
    *, db: Session = Depends(get_db), user_id: int, limits: dict = Depends(get_limits)
):
    """Returns a list of conversations linked to a user."""
    crud.user.get_or_404(db, id=user_id)
    return crud.conversation.get_user(db, user_id=user_id, **limits)


@router.get(
    "",
    response_model=List[Conversation],
    summary="Get all conversations",
    response_description="List of transcripted conversations",
)
def conversations_get_from_all_users(
    *, db: Session = Depends(get_db), limits: dict = Depends(get_limits)
):
    """Returns a list of all conversations."""
    return crud.conversation.get_multi(db, **limits)


@router.delete(
    "/{conversation_id}",
    response_class=Response,
    response_description="Transcripted conversation removed successfully",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove a conversation",
    **gen_responses({404: "Conversation not found"}),
)
def conversation_delete(*, db: Session = Depends(get_db), conversation_id: int):
    """Removes a conversation using its id."""
    crud.conversation.remove(db, id=conversation_id)
