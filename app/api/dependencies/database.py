"""Database dependencies."""

from app.db.session import SessionLocal, engine


async def get_db():
    """Creates a local database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        engine.dispose()
