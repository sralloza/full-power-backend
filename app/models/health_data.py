"""Database models."""

from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime

from app.db.base_class import Base

# pylint: disable=too-few-public-methods


class HealthData(Base):
    """Represents a conversation between a user and the health bot."""

    __tablename__ = "health-data"

    id = Column(Integer, primary_key=True, index=True)
    get_up = Column(Boolean)
    sleep = Column(Boolean)
    screen = Column(Boolean)
    bedroom = Column(Boolean)
    stress = Column(Boolean)
    timestamp = Column(DateTime)
    valid = Column(Boolean, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User")
