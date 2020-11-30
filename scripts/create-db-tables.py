import logging
import warnings

from app.db.init_db import init_db
from app.db.session import SessionLocal

warnings.warn(
    "Don't use this, use always 'alembic upgrade' to setup the database tables"
)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    db = SessionLocal()
    init_db(db)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
