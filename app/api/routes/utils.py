"""Routes for utils."""

from fastapi import APIRouter, Depends, Security

from app import __version__
from app.api.dependencies.security import get_current_user
from app.core.config import Settings, settings
from app.schemas.user import User

router = APIRouter()


@router.get("/", summary="Get server state")
def state():
    return {"detail": "backend server online"}


@router.get("/version", summary="Get server version")
def get_version():
    return {"version": __version__}


@router.get(
    "/settings",
    dependencies=[Security(get_current_user, scopes=["admin"])],
    response_model=Settings,
    summary="Get server settings",
)
def get_settings():
    """Returns the current api settings. Requires admin."""

    return settings


@router.get("/me", response_model=User, summary="Get logged user")
def users_get_current_user(current_user: User = Depends(get_current_user)):
    """Returns the current user."""

    return current_user
