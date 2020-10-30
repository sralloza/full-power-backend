from app.db.session import SessionLocal, engine


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        engine.dispose()
