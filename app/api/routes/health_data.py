"""Health data related routes."""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm.session import Session
from starlette.responses import Response

from app import crud
from app.api.dependencies.database import get_db
from app.api.dependencies.utils import get_limits
from app.schemas.health_data import HealthData, HealthDataCreate

router = APIRouter()


@router.post(
    "",
    response_model=HealthData,
    status_code=status.HTTP_201_CREATED,
    summary="Create health data results",
)
def health_data_create_post(
    *, db: Session = Depends(get_db), health_data: HealthDataCreate
):
    """Create a health data result."""
    return crud.health_data.create(db, obj_in=health_data)


@router.get(
    "/user/{user_id}",
    response_model=List[HealthData],
    summary="Get health data results from a user",
    responses={404: {"description": "User not found"}},
)
def health_data_get_from_user(
    *, db: Session = Depends(get_db), user_id: int, limits: dict = Depends(get_limits)
):
    """Get health data results from a user given its id."""
    crud.user.get_or_404(db, id=user_id)
    return crud.health_data.get_user(db, user_id=user_id, **limits)


@router.get(
    "/{health_data_id}",
    response_model=HealthData,
    summary="Get health data results by id",
    responses={404: {"description": "Health data results not found"}},
)
def get_health_data_by_id(*, db: Session = Depends(get_db), health_data_id: int):
    """Get health data results given its id."""
    return crud.health_data.get_or_404(db, id=health_data_id)


@router.get(
    "",
    response_model=List[HealthData],
    summary="Get health data results from all users",
)
def health_data_get_from_all_users(
    *, db: Session = Depends(get_db), limits: dict = Depends(get_limits)
):
    """Get health data results from all users."""
    return crud.health_data.get_multi(db, **limits)


@router.delete(
    "/{health_data_id}",
    response_class=Response,
    responses={404: {"description": "Health data not found"}},
    status_code=204,
    summary="Remove health data result",
)
def health_data_delete(*, db: Session = Depends(get_db), health_data_id: int):
    """Remove health data result given its id."""
    crud.health_data.remove(db, id=health_data_id)
