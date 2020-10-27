"""Manage database connections involving conversations data."""

import logging

from fastapi import HTTPException

from app.database import db, models
from .users import get_user

from . import schemas

logger = logging.getLogger(__name__)


def list_user_conversations(user_id: int, skip: int = 0, limit: int = 100):
    """Lists all conversations for a given user."""

    return (
        db.query(models.Conversation)
        .filter_by(user_id=user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def list_all_conversations(skip: int = 0, limit: int = 100):
    """Lists all conversations for all users."""

    return db.query(models.Conversation).offset(skip).limit(limit).all()


def create_conversation(conversation: schemas.ConversationCreate, user_id: int):
    """Saves a conversation to the database."""
    conv = models.Conversation(**conversation.dict(), user=get_user(user_id))
    db.add(conv)
    db.commit()
    db.refresh(conv)

    logger.debug("Conversation created for user_id=%d (conv_id=%d)", user_id, conv.id)
    return conv


def remove_conversation(conversation_id: int):
    """Removes a conversation from the database."""

    conv = db.query(models.Conversation).filter_by(id=conversation_id).first()
    if not conv:
        logger.warning("Conversation id=%d does not exist", conv.id)
        raise HTTPException(404, f"Conversation id={conversation_id} does not exist")

    db.delete(conv)
    db.commit()

    logger.debug("Removed conversation id=%d", conv.id)
