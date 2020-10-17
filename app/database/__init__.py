import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
assert SQLALCHEMY_DATABASE_URL, "Must set SQLALCHEMY_DATABASE_URL environ variable"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db: Session = SessionLocal()


class _Base:
    def dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}


Base = declarative_base(cls=_Base)
