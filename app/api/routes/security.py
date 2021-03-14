"""Routes involving security, like /login and /register."""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from app import __version__, crud
from app.api.dependencies.database import get_db
from app.api.dependencies.security import get_current_user
from app.core.config import settings
from app.core.security import authenticate_user, create_access_token
from app.schemas.token import Token
from app.schemas.user import UserCreateAdmin, UserCreateBasic, UserPublic

router = APIRouter(tags=["Security"])


@router.post(
    "/login",
    response_model=Token,
    responses={401: {"description": "Incorrect username of password"}},
    summary="Grants access to users",
)
def login_post(
    *,
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
    response: Response
):
    """Login endpoint."""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.token_expire_minutes)
    crud.user.set_last_login_now(db, id=user.id)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": user.scopes},
        expires_delta=access_token_expires,
    )
    response.headers["X-Current-User"] = UserPublic.from_orm(user).json()
    return Token(access_token=access_token, scopes=user.scopes)


@router.post(
    "/register",
    response_model=UserPublic,
    responses={409: {"description": "Username already registered"}},
    status_code=201,
    summary="Register new user",
)
def register_basic_user(*, db: Session = Depends(get_db), user: UserCreateBasic):
    """Register endpoint."""
    real_user = UserCreateAdmin(**user.dict(), is_admin=False)
    return crud.user.create(db, obj_in=real_user)


@router.post("/refresh", response_model=Token, summary="Update token")
def refresh_post(user=Depends(get_current_user)):
    """Endpoint to create a new valid token."""
    access_token_expires = timedelta(minutes=settings.token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": user.scopes},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, scopes=user.scopes)
