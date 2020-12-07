"""Health data related routes."""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from starlette.responses import Response

from app import crud
from app.api.dependencies.database import get_db
from app.schemas.health_data import HealthData, HealthDataCreate

router = APIRouter()


@router.post("", response_model=HealthData, summary="Create health data results")
def health_data_create_post(
    *, db: Session = Depends(get_db), health_data: HealthDataCreate
):
    """Create a health data result."""
    return crud.health_data.create(db, obj_in=health_data)


@router.get(
    "/user/{user_id}",
    response_model=List[HealthData],
    summary="Get health data results from a user",
)
def health_data_get_from_user(
    *, db: Session = Depends(get_db), user_id: int, skip: int = 0, limit: int = 100
):
    """Get health data results from a user given its id."""
    return crud.health_data.get_user(db, user_id=user_id, skip=skip, limit=limit)


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
    *, db: Session = Depends(get_db), skip: int = 0, limit: int = 100
):
    """Get health data results from all users."""
    return crud.health_data.get_multi(db, skip=skip, limit=limit)


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
