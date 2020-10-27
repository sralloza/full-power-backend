"""Database models."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.db.base_class import Base

# pylint: disable=too-few-public-methods


class Conversation(Base):
    """Represents a conversation between a user and the health bot."""

    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_msg = Column(String(200), index=True, nullable=False)
    bot_msg = Column(String(200), index=True, nullable=False)
    intent = Column(String(50), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="conversations")
