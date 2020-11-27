"""Conversations manager."""

from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from starlette.responses import Response

from app import crud
from app.api.dependencies.database import get_db
from app.schemas.health_data import HealthData, HealthDataCreate

router = APIRouter()


@router.post("", response_model=HealthData)
def health_data_create_post(
    *, db: Session = Depends(get_db), health_data: HealthDataCreate
):
    return crud.health_data.create(db, obj_in=health_data)


@router.get("/user/{user_id}", response_model=List[HealthData])
def health_data_get_from_user(
    *, db: Session = Depends(get_db), user_id: int, skip: int = 0, limit: int = 100
):
    return crud.health_data.get_user(db, user_id=user_id, skip=skip, limit=limit)


@router.get("", response_model=List[HealthData])
def health_data_get_from_all_users(
    *, db: Session = Depends(get_db), skip: int = 0, limit: int = 100
):
    return crud.health_data.get_multi(db, skip=skip, limit=limit)


@router.delete(
    "/{health_data_id}",
    responses={404: {"description": "Health data not found"}},
    status_code=204,
)
def health_data_delete(*, db: Session = Depends(get_db), health_data_id: int):
    crud.health_data.remove(db, id=health_data_id)
    return Response(status_code=HTTPStatus.NO_CONTENT.value)
