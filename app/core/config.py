"""Internal settings of the API."""

import logging
import os
import secrets
from enum import Enum
from pathlib import Path

from pydantic import BaseSettings, FilePath, confloat


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

    # General
    production: bool = False

    # Security
    encryption_algorithm: str = "HS256"
    server_secret: str = secrets.token_urlsafe(32)
    token_expire_minutes: int = 30

    # Database
    first_superuser_password: str
    first_superuser: str
    sqlalchemy_database_url: str

    # Dialogflow
    dialogflow_project_id: str
    google_application_credentials: FilePath

    # Logging
    log_path: Path
    logging_level: ValidLoggingLevel = ValidLoggingLevel.INFO
    max_logs: int = 30

    # HealthData parsing
    problem_ratio_threshold: confloat(ge=0, le=1) = 0.75

    # Testing
    username_test_user: str = "the_Test"
    username_test_password: str = "the_TestPassword"

    class Config:
        env_file = Path(__file__).parent.parent.with_name(".env").as_posix()
        env_file_encoding = "utf-8"

    def set_environment(self):
        os.environ[
            "GOOGLE_APPLICATION_CREDENTIALS"
        ] = self.google_application_credentials.as_posix()


settings = Settings()
settings.set_environment()
