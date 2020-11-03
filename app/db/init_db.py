from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.db.base_class import Base
from app.db.session import engine
from app.schemas.user import UserCreateAdmin


def init_db(db: Session) -> None:
    Base.metadata.create_all(bind=engine)

    user = crud.user.get_by_username(db, username=settings.first_superuser)
    if not user:
        user_in = UserCreateAdmin(
            username=settings.first_superuser,
            password=settings.first_superuser_password,
            is_admin=True,
        )
        user = crud.user.create(db, obj_in=user_in)

    db.commit()
