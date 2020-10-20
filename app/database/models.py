"""Database models."""

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from . import Base

# pylint: disable=too-few-public-methods


class User(Base):
    """Represents a user."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(200))
    is_admin = Column(Boolean, default=True)

    conversations = relationship("Conversation", back_populates="user")

    @property
    def scopes(self):
        """Determines the permissions of the user."""

        if self.is_admin:
            return ["admin", "basic"]
        return ["basic"]


class Conversation(Base):
    """Represents a conversation between a user and the health bot."""

    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_msg = Column(String(200), index=True, nullable=False)
    bot_msg = Column(String(200), index=True, nullable=False)
    intent = Column(String(50), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="conversations")
