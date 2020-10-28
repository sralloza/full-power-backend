"""Database basic connections."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

if "sqlite" in settings.sqlalchemy_database_url:
    connect_args = {"check_same_thread": False}
else:
    connect_args = {}

engine = create_engine(
    settings.sqlalchemy_database_url, pool_pre_ping=True, connect_args=connect_args
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
