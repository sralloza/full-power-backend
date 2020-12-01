import logging

logging.basicConfig(level=logging.INFO)

from sqlalchemy.orm.session import Session

from app import crud
from app.core.config import settings
from app.db.session import SessionLocal
from app.schemas.user import UserCreateAdmin

logger = logging.getLogger(__name__)


def create_first_admin(db: Session):
    user = crud.user.get_by_username(db, username=settings.first_superuser)
    if user:
        logger.info("User was already created")
        return

    user_in = UserCreateAdmin(
        username=settings.first_superuser,
        password=settings.first_superuser_password,
        is_admin=True,
    )
    user = crud.user.create(db, obj_in=user_in)

    db.commit()
    logger.info("User created")


def main():
    logger.info("Starting create-first-admin script")

    db = SessionLocal()
    create_first_admin(db)

    logger.info("create-first-admin script ended")


if __name__ == "__main__":
    main()
