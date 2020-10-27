"""Internal settings of the API."""

import logging
import os
import secrets
from enum import Enum
from pathlib import Path

from pydantic import AnyUrl, BaseSettings, FilePath, conint, validator
from pydantic.types import PositiveInt


class SqlUrl(AnyUrl):
    allowed_schemes = {"mysql+pymysql"}
    user_required = True


class ValidLoggingLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

    def as_python_logging(self):
        return logging._nameToLevel[self.value]


class Settings(BaseSettings):
    """Internal settings of the API"""

    dialogflow_project_id: str
    encryption_algorithm: str = "HS256"
    google_application_credentials: FilePath
    log_path: FilePath
    logging_level: ValidLoggingLevel = ValidLoggingLevel.INFO
    max_logs: int = 30
    production: bool = False
    server_secret: str = secrets.token_urlsafe(32)
    sqlalchemy_database_url: SqlUrl

    @validator("sqlalchemy_database_url")
    def check_db_name(cls, v):
        assert v.path and len(v.path) > 1, "database must be provided"
        return v

    token_expire_minutes: int = 30

    first_superuser_password: str
    first_superuser: str

    class Config:
        env_file = Path(__file__).parent.parent.with_name(".env").as_posix()
        env_file_encoding = "utf-8"

    def set_environment(self):
        os.environ[
            "GOOGLE_APPLICATION_CREDENTIALS"
        ] = self.google_application_credentials.as_posix()

    username_test_user: str = "the_Test"


settings = Settings()
settings.set_environment()
