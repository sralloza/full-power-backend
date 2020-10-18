"""Internal settings of the API."""

from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Internal settings of the API"""

    sqlalchemy_database_url: str
    production: bool = False

    class Config:
        env_file = Path(__file__).parent.with_name(".env").as_posix()


settings = Settings()
