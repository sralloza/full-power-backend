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

    energy = Column(Integer)
    restful_sleep = Column(Integer)
    fall_asleep_easily = Column(Integer)
    deep_sleep = Column(Integer)
    enough_sleep = Column(Integer)
    energy_morning = Column(Integer)

    uniform_mood = Column(Integer)
    memory = Column(Integer)
    concentration = Column(Integer)
    creativity = Column(Integer)
    stress = Column(Integer)
    cramps = Column(Integer)
    dagger = Column(Integer)

    pump_strokes = Column(Integer)
    uplifts = Column(Integer)
    swollen_belly = Column(Integer)
    gases = Column(Integer)
    bowel_movement = Column(Integer)
    sheet_wipe = Column(Integer)

    timestamp = Column(DateTime)
    valid = Column(Boolean, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User")
