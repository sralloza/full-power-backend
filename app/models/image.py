from sqlalchemy import Column, Integer
from sqlalchemy.sql.sqltypes import LargeBinary, String

from app.db.base_class import Base

# pylint: disable=too-few-public-methods


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    image_type = Column(String(100), nullable=False)
    mime_type = Column(String(100), nullable=False)
    content = Column(LargeBinary(2 * 1024 * 1024), nullable=False)
