"""Security dependencies."""

from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer, SecurityScopes
from jose import ExpiredSignatureError, JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm.session import Session

from app import crud
from app.core.config import settings
from app.schemas.token import TokenData

from .database import get_db

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login", scopes={"admin": "admin stuff", "basic": "rest of users"}
)


def get_current_user(
    *,
    db: Session = Depends(get_db),
    sec_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
):
    """Returns the current user, given the token present in the header.

    Returns 401 on any error.
    """
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
        payload = jwt.decode(
            token, settings.server_secret, algorithms=[settings.encryption_algorithm]
        )
        username = payload.get("sub")

        if username is None:
            credentials_exception.headers["X-Login-Error"] = "No username in token"
            raise credentials_exception

        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except ExpiredSignatureError as exc:
        credentials_exception.headers["X-Login-Error"] = "Token expired"
        raise credentials_exception from exc
    except (JWTError, ValidationError) as exc:
        credentials_exception.headers["X-Login-Error"] = "Invalid token"
        raise credentials_exception from exc

    user = crud.user.get_by_username(db, username=token_data.username)
    if user is None:
        credentials_exception.headers["X-Login-Error"] = "Invalid username"
        raise credentials_exception

    for scope in sec_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not enough permissions [{scope} access required]",
                headers={"WWW-Authenticate": authenticate_value},
            )

    crud.user.set_last_login_now(db, id=user.id)
    return user
