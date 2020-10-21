"""Routes involving security, like /login and /register."""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.param_functions import Security
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app import __version__
from app.config import Settings, settings
from app.users.crud import create_user
from app.users.schemas import BasicUserCreate, UserCreate, UserPublic

from .schemas import Token
from .utils import authenticate_user, create_access_token, get_current_user

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()


@router.get("/")
def state():
    return {"detail": "backend server online"}


@router.get("/version")
def get_version():
    return {"version": __version__}


@router.post("/login", response_model=Token)
def login_post(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login endpoint."""

    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": user.scopes},
        expires_delta=access_token_expires,
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_minutes": ACCESS_TOKEN_EXPIRE_MINUTES,
        "scopes": user.scopes,
    }


@router.post(
    "/register",
    response_model=UserPublic,
    responses={400: {"description": "Username already registered"}},
)
def register_basic_user(user: BasicUserCreate):
    """Register endpoint."""

    real_user = UserCreate(**user.dict(), is_admin=False)
    return create_user(real_user)


@router.post("/refresh", response_model=Token)
def login_post(user=Depends(get_current_user)):
    """Login endpoint."""

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": user.scopes},
        expires_delta=access_token_expires,
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_minutes": ACCESS_TOKEN_EXPIRE_MINUTES,
        "scopes": user.scopes,
    }


@router.get(
    "/settings",
    dependencies=[Security(get_current_user, scopes=["admin"])],
    response_model=Settings,
)
def get_settings():
    """Returns the current api settings. Requires admin."""

    return settings
