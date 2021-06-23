"""Routes for managing users (most of them require admin access, except /me)."""

from typing import List

from fastapi import APIRouter, Depends, Response, Security
from sqlalchemy.orm.session import Session

from app import crud
from app.api.dependencies.database import get_db
from app.api.dependencies.security import get_current_user
from app.api.dependencies.utils import get_limits
from app.schemas.user import UserCreateAdmin, UserInDB
from app.utils.responses import gen_responses

router = APIRouter(
    dependencies=[Security(get_current_user, scopes=["admin"])],
    prefix="/users",
    tags=["Users"],
    **gen_responses({401: "Admin access required"}),
)


@router.post(
    "",
    response_description="The created user",
    response_model=UserInDB,
    status_code=201,
    summary="Create new user",
    **gen_responses({409: "Username already registered"}),
)
def users_create_post(*, db: Session = Depends(get_db), user: UserCreateAdmin):
    """Creates a new user (can be admin, unlike in /register)."""
    return crud.user.create(db, obj_in=user)


@router.get(
    "",
    response_description="List of users",
    response_model=List[UserInDB],
    summary="List all users",
)
def users_list_all(
    *, db: Session = Depends(get_db), limits: dict = Depends(get_limits)
):
    """Returns all users."""
    users = crud.user.get_multi(db, **limits)
    return users


@router.get(
    "/{user_id}",
    response_description="The user",
    response_model=UserInDB,
    summary="Get user by id",
    **gen_responses({404: "User not found"}),
)
def users_get_one(*, db: Session = Depends(get_db), user_id: int):
    """Returns a user by its id."""
    return crud.user.get_or_404(db, id=user_id)


@router.delete(
    "/{user_id}",
    response_class=Response,
    response_description="User deleted successfully",
    status_code=204,
    summary="Delete user",
    **gen_responses({404: "User not found"}),
)
def users_delete(*, db: Session = Depends(get_db), user_id: int):
    """Deletes a user."""
    crud.user.remove(db, id=user_id)
