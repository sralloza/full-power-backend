"""Data schematics for security endpoints."""

from typing import List

from pydantic import BaseModel


class TokenData(BaseModel):
    """Represents a token decrypted. Used only in backend."""

    username: str
    scopes: List[str] = []


class Token(BaseModel):
    """Token data returned to the user after login."""

    access_token: str
    token_type: str
    expires_minutes: int
