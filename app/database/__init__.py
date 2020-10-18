"""Database basic connections."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from app.config import settings

engine = create_engine(
    settings.sqlalchemy_database_url, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db: Session = SessionLocal()


class _Base:  # pylint: disable=too-few-public-methods
    """Base class for models."""

    def dict(self):
        """Returns the attributes of self as a dict, like pydantic.Model."""

        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}


Base = declarative_base(cls=_Base)
