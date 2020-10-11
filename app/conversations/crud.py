from app.database import db, models
from app.users.crud import get_user

from . import schemas


def list_user_conversations(user_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Conversation)
        .filter_by(user_id=user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def list_all_conversations(skip: int = 0, limit: int = 100):
    return db.query(models.Conversation).offset(skip).limit(limit).all()


def create_conversation(conversation: schemas.ConversationCreate, user_id: int):
    db_item = models.Conversation(**conversation.dict(), user=get_user(user_id))
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
