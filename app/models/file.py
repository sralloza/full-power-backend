from sqlalchemy import Column, Text, String

from app.db.base_class import Base

# pylint: disable=too-few-public-methods


class File(Base):
    __tablename__ = "files"

    id = Column(String(100), primary_key=True, index=True)
    lang = Column(String(10), index=True, nullable=False)
    name = Column(String(100), index=True, nullable=False)
    title = Column(String(100), index=True, nullable=False)
    content = Column(Text(20_000), nullable=False)
