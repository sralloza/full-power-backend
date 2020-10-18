"""Security utils."""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from app.database.models import User

from .schemas import TokenData

SECRET_KEY = "bc1994fc98b4757f41cadf698c28bb06a6a560f59f74c27c9e81e71304f78010"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login", scopes={"admin": "admin stuff", "basic": "rest of users"}
)


def authenticate_user(username: str, hashed_password: str) -> Optional[User]:
    """Given a username and a hashed password, returns the user from the
    database if the username and the hashed passwords are valid.
    """

    # pylint: disable=import-outside-toplevel
    from app.users.crud import get_user_by_username

    user = get_user_by_username(username)
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
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(sec_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    """Returns the current user, given the token present in the header.

    Returns 401 on any error.

    """

    # pylint: disable=import-outside-toplevel
    from app.users.crud import get_user_by_username

    if sec_scopes.scopes:
        authenticate_value = f'Bearer scope="{sec_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError) as exc:
        raise credentials_exception from exc

    user = get_user_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception

    for scope in sec_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Not enough permissions [{scope} required]",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Returns True if passwords match, False otherwise."""

    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Returns the hash of the password."""

    return pwd_context.hash(password)


def debug_token(token):
    """Used for debugging, decrypts a token."""

    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
