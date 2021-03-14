"""Routes for utils."""

from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session
from starlette.responses import Response

from app import __version__, crud
from app.api.dependencies.database import get_db
from app.api.dependencies.security import get_current_user
from app.core.config import Settings, settings
from app.models import User
from app.schemas.user import UserPublic, UserUpdateAdmin

router = APIRouter(tags=["Utils"])


@router.get("/", summary="Get server state")
def state():
    """Returns the status of the server."""
    return {"detail": "backend server online"}


@router.get("/version", summary="Get server version")
def get_version():
    """Returns the version of the server."""
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


@router.get("/me", response_model=UserPublic, summary="Get logged user")
def users_get_current_user(current_user: User = Depends(get_current_user)):
    """Returns the current user."""

    return current_user


@router.post(
    "/accept-disclaimer", response_class=Response, summary="User accepts disclaimer"
)
def accept_disclaimer(
    db: Session = Depends(get_db), *, current_user: User = Depends(get_current_user)
):
    """Accepts the disclaimer."""

    user = UserUpdateAdmin(accepted_disclaimer=True)
    crud.user.update(db, db_obj=current_user, obj_in=user)


@router.post("/survey-filled", response_class=Response, summary="User fills survey")
def survey_filled(
    db: Session = Depends(get_db), *, current_user: User = Depends(get_current_user)
):
    """Accepts the disclaimer."""

    user = UserUpdateAdmin(survey_filled=True)
    crud.user.update(db, db_obj=current_user, obj_in=user)
