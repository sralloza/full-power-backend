"""Database models."""

from sqlalchemy import Boolean, Column, Integer, String, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime

from app.db.base_class import Base

# pylint: disable=too-few-public-methods


class User(Base):
    """Represents a user."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(200))
    is_admin = Column(Boolean, default=False)
    last_login = Column(DateTime, server_default=func.now(), onupdate=func.now())
    survey_filled = Column(Boolean, default=False, nullable=False)
    accepted_disclaimer = Column(Boolean, default=False, nullable=False)

    conversations = relationship("Conversation", back_populates="user")
    health_data = relationship("HealthData", back_populates="user")

    @property
    def scopes(self):
        """Determines the permissions of the user."""

        if self.is_admin:
            return ["admin", "basic"]
        return ["basic"]
