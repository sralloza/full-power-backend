"""Routes involving security, like /login and /register."""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from app import __version__, crud
from app.api.dependencies.database import get_db
from app.api.dependencies.security import get_current_user
from app.core.config import Settings, settings
from app.core.security import authenticate_user, create_access_token
from app.schemas.token import Token
from app.schemas.user import User, UserCreateAdmin, UserCreateBasic

router = APIRouter()


@router.get("/")
def state():
    return {"detail": "backend server online"}


@router.get("/version")
def get_version():
    return {"version": __version__}


@router.post("/login", response_model=Token)
def login_post(
    *, db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
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
    access_token = create_access_token(
        data={"sub": user.username, "scopes": user.scopes},
        expires_delta=access_token_expires,
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_minutes": access_token_expires.seconds // 60,
        "scopes": user.scopes,
    }


@router.post(
    "/register",
    response_model=User,
    responses={400: {"description": "Username already registered"}},
)
def register_basic_user(*, db: Session = Depends(get_db), user: UserCreateBasic):
    """Register endpoint."""

    real_user = UserCreateAdmin(**user.dict(), is_admin=False)
    return crud.user.create(db, obj_in=real_user)


@router.post("/refresh", response_model=Token)
def refresh_post(user=Depends(get_current_user)):
    """Login endpoint."""

    access_token_expires = timedelta(minutes=settings.token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": user.scopes},
        expires_delta=access_token_expires,
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_minutes": access_token_expires.seconds // 60,
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


@router.get("/me", response_model=User)
def users_get_current_user(current_user: User = Depends(get_current_user)):
    """Returns the current user."""

    return current_user
