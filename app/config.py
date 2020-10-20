"""Internal settings of the API."""

import os
from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Internal settings of the API"""

    dialogflow_project_id: str
    google_application_credentials: str
    production: bool = False
    sqlalchemy_database_url: str

    class Config:
        env_file = Path(__file__).parent.with_name(".env").as_posix()
        env_file_encoding = "utf-8"
        fields = {
            "dialogflow_project_id": {"env": "DIALOGFLOW_PROJECT_ID"},
            "google_application_credentials": {"env": "GOOGLE_APPLICATION_CREDENTIALS"},
        }

    def set_environment(self):
        os.environ[
            "GOOGLE_APPLICATION_CREDENTIALS"
        ] = self.google_application_credentials


settings = Settings()
settings.set_environment()
