"""Internal settings of the API."""

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv(Path(__file__).parent.with_name(".env"))

class Settings(BaseSettings):
    """Internal settings of the API"""
    sqlalchemy_database_url = os.getenv("SQLALCHEMY_DATABASE_URL")

    assert sqlalchemy_database_url, "Must set SQLALCHEMY_DATABASE_URL environ variable"


settings = Settings()
