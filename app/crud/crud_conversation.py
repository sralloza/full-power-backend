"""Manage database connections involving conversations data."""

import logging
import re

from sqlalchemy.orm.session import Session

from app.crud.base import CRUDBase
from app.models.conversation import Conversation
from app.schemas.conversation import ConversationCreate, ConversationUpdate, DisplayType

logger = logging.getLogger(__name__)


class CRUDConversation(CRUDBase[Conversation, ConversationCreate, ConversationUpdate]):
    def create(self, db: Session, *, obj_in: ConversationCreate) -> Conversation:
        obj_in.display_type = DisplayType.default
        if re.search(r"\d", obj_in.intent) and "19" not in obj_in.intent:
            obj_in.display_type = DisplayType.five_stars

        return super().create(db, obj_in=obj_in)

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
