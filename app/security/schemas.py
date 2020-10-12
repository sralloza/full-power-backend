from typing import Optional

from pydantic.main import BaseModel


class TokenData(BaseModel):
    username: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    id: int
    username: str


class DBUser(User):
    hashed_password: str

    class Config:
        orm_mode = True
