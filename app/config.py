"""Internal settings of the API."""

import os
from pathlib import Path

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Internal settings of the API"""

    dialogflow_project_id: str = Field(..., env="DIALOGFLOW_PROJECT_ID")
    google_application_credentials: str = Field(
        ..., env="GOOGLE_APPLICATION_CREDENTIALS"
    )
    production: bool = Field(False, env="PRODUCTION")
    sqlalchemy_database_url: str = Field(..., env="SQLALCHEMY_DATABASE_URL")

    class Config:
        env_file = Path(__file__).parent.with_name(".env").as_posix()
        env_file_encoding = "utf-8"

    def set_environment(self):
        os.environ[
            "GOOGLE_APPLICATION_CREDENTIALS"
        ] = self.google_application_credentials


settings = Settings()
settings.set_environment()
