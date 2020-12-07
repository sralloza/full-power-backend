"""Data schematics for security endpoints."""

from typing import List

from pydantic import BaseModel, Field

from app.core.config import settings


class TokenData(BaseModel):
    """Represents a token decrypted. Used only in backend."""

    username: str
    scopes: List[str]


class Token(BaseModel):
    """Token data returned to the user after login."""

    access_token: str
    token_type: str = "Bearer"
    expires_minutes: int = Field(default_factory=lambda: settings.token_expire_minutes)
    scopes: List[str]
