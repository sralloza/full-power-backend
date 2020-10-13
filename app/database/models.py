from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=True)

    conversations = relationship("Conversation", back_populates="user")

    @property
    def scopes(self):
        if self.is_admin:
            return ["admin", "basic"]
        return ["basic"]


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_msg = Column(String, index=True, nullable=False)
    bot_msg = Column(String, index=True, nullable=False)
    intent = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="conversations")
