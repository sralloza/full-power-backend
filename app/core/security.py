"""Security utils."""

from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm.session import Session

from app import crud
from app.core.config import settings
from app.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(
    db: Session, username: str, hashed_password: str
) -> Optional[User]:
    """Given a username and a hashed password, returns the user from the
    database if the username and the hashed passwords are valid.
    """

    user = crud.user.get_by_username(db, username=username)
    if not user:
        return None
    if not verify_password(hashed_password, user.hashed_password):
        return None

    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Encrypts the data to create a expirable token."""

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.server_secret, algorithm=settings.encryption_algorithm
    )
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Returns True if passwords match, False otherwise."""

    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Returns the hash of the password."""

    return pwd_context.hash(password)


def debug_token(token):  # noqa
    """Used for debugging, decrypts a token."""

    return jwt.decode(
        token, settings.server_secret, algorithms=[settings.encryption_algorithm]
    )
