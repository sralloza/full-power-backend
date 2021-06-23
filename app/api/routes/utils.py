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
from app.utils.responses import Message, Version, gen_responses

router = APIRouter(tags=["Utils"])


@router.get(
    "/",
    response_description="Server online",
    response_model=Message,
    summary="Get server state",
)
def state():
    """Returns the status of the server."""
    return {"detail": "backend server online"}


@router.get(
    "/version",
    response_description="The backend's version",
    response_model=Version,
    summary="Get server version",
)
def get_version():
    """Returns the version of the server."""
    return {"version": __version__}


@router.get(
    "/settings",
    dependencies=[Security(get_current_user, scopes=["admin"])],
    response_description="Current server settings",
    response_model=Settings,
    summary="Get server settings",
    **gen_responses({403: "Admin access required"}),
)
def get_settings():
    """Returns the current api settings. Requires admin."""
    return settings


@router.get(
    "/me",
    response_description="The current user's personal info",
    response_model=UserPublic,
    summary="Get logged user",
    **gen_responses({401: "User not logged in"}),
)
def users_get_me(current_user: User = Depends(get_current_user)):
    """Returns the current user."""
    return current_user


@router.post(
    "/accept-disclaimer",
    response_class=Response,
    response_description="Operation successfull",
    summary="User accepts the disclaimer",
    **gen_responses({401: "User not logged in"}),
)
def accept_disclaimer(
    db: Session = Depends(get_db), *, current_user: User = Depends(get_current_user)
):
    """User accepts the disclaimer."""
    user = UserUpdateAdmin(accepted_disclaimer=True)
    crud.user.update(db, db_obj=current_user, obj_in=user)


@router.post(
    "/survey-filled",
    response_class=Response,
    response_description="Operation successfull",
    summary="User fills the first survey",
    **gen_responses({401: "User not logged in"}),
)
def survey_filled(
    db: Session = Depends(get_db), *, current_user: User = Depends(get_current_user)
):
    """User fills the first survey."""
    user = UserUpdateAdmin(survey_filled=True)
    crud.user.update(db, db_obj=current_user, obj_in=user)
