"""Internal settings of the API."""

import logging
import os
from enum import Enum
from pathlib import Path

from pydantic import BaseSettings, Field, validator


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

    dialogflow_project_id: str = Field(..., env="DIALOGFLOW_PROJECT_ID")
    google_application_credentials: str = Field(
        ..., env="GOOGLE_APPLICATION_CREDENTIALS"
    )
    log_path: str = Field(..., env="LOG_PATH")
    logging_level: ValidLoggingLevel = Field(
        ValidLoggingLevel.INFO, env="LOGGING_LEVEL"
    )
    max_logs: int = Field(0, env="MAX_LOGS")
    production: bool = Field(False, env="PRODUCTION")
    server_secret: str = Field(..., env="SECRET")
    sqlalchemy_database_url: str = Field(..., env="SQLALCHEMY_DATABASE_URL")
    token_expire_minutes: int = Field(30, env="TOKEN_EXPIRE_MINUTES")
    encryption_algorithm: str = "HS256"

    @validator("server_secret")
    def validate_secret(cls, value):
        if len(value) != 64:
            raise ValueError("SECRET must contain 64 characters")
        return value

    class Config:
        env_file = Path(__file__).parent.parent.with_name(".env").as_posix()
        env_file_encoding = "utf-8"

    def set_environment(self):
        os.environ[
            "GOOGLE_APPLICATION_CREDENTIALS"
        ] = self.google_application_credentials


settings = Settings()
settings.set_environment()
