from sqlalchemy.orm import Session

from app import crud
from app.schemas.user import UserCreateAdmin
from app.core.config import settings


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    # TODO: make this configurable via settings
    user = crud.user.get_by_username(db, username="admin")
    if not user:
        user_in = UserCreateAdmin(
            username="admin",
            password="1234",
            admin=True,
        )
        user = crud.user.create(db, obj_in=user_in)
