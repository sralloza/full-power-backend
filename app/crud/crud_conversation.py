"""Manage database connections involving conversations data."""

import logging

from fastapi import HTTPException
from sqlalchemy.orm.session import Session

from app.crud.base import CRUDBase
from app.crud.crud_conversation import CRUDConversation
from app.models.conversation import Conversation
from app.schemas.conversation import ConversationCreate

logger = logging.getLogger(__name__)


class CRUDConversation(CRUDBase[Conversation, ConversationCreate, None]):
    def get_user(self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100):
        """Lists all conversations for a given user."""

        return (
            db.query(self.model)
            .filter_by(user_id=user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )



conversation = CRUDConversation(Conversation)
