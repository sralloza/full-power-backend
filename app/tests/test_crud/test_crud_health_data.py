from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.schemas.health_data import HealthDataUpdate
from app.tests.utils.health_data import gen_health_data_create
from app.tests.utils.utils import random_constrained_int, random_int


def test_create_health_data(db: Session):
    user_id = random_int()
    health_data_in = gen_health_data_create(user_id, True)
    health_data_db = crud.health_data.create(db, obj_in=health_data_in)

    assert health_data_db.user_id == user_id
    assert health_data_db.valid == health_data_in.valid
    assert health_data_db.stress == health_data_in.stress
    assert health_data_db.pump_strokes == health_data_in.pump_strokes
    assert hasattr(health_data_db, "id")
    assert health_data_db.id


def test_get_health_data(db: Session):
    user_id = random_int()
    health_data_in = gen_health_data_create(user_id, True)
    health_data_db = crud.health_data.create(db, obj_in=health_data_in)
    health_data_db_2 = crud.health_data.get(db, id=health_data_db.id)

    assert health_data_db_2
    assert health_data_db_2.user_id == health_data_db.user_id
    assert health_data_db_2.pump_strokes == health_data_db.pump_strokes
    assert health_data_db_2.dagger == health_data_db.dagger
    assert health_data_db_2.stress == health_data_db.stress
    assert health_data_db_2.id == health_data_db.id
    assert jsonable_encoder(health_data_db) == jsonable_encoder(health_data_db_2)


def test_get_pending_health_data(db: Session):
    user_id = random_int()
    hd_in_1 = crud.health_data.create(db, obj_in=gen_health_data_create(user_id, True))
    hd_in_2 = crud.health_data.create(db, obj_in=gen_health_data_create(user_id, False))

    pending_health_data = crud.health_data.get_pending_from_user(db, user_id=user_id)
    assert pending_health_data == hd_in_2
    assert pending_health_data != hd_in_1


def test_update_health_data(db: Session):
    user_id = random_int()
    health_data_in = gen_health_data_create(user_id, True)
    health_data_db = crud.health_data.create(db, obj_in=health_data_in)

    new_dagger = random_constrained_int(1, 5)
    new_stress = random_constrained_int(1, 5)
    health_data_in_update = HealthDataUpdate(dagger=new_dagger, stress=new_stress)
    crud.health_data.update(db, db_obj=health_data_db, obj_in=health_data_in_update)
    health_data_db_2 = crud.health_data.get(db, id=health_data_db.id)

    assert health_data_db_2
    assert health_data_db_2.user_id == user_id
    assert health_data_db_2.dagger == new_dagger
    assert health_data_db_2.stress == new_stress


def test_get_health_data_from_user(db: Session):
    user_id = random_int()
    health_datas = []
    for _ in range(7):
        health_data_in = gen_health_data_create(user_id, True)
        health_datas.append(crud.health_data.create(db, obj_in=health_data_in))

    real_convs = crud.health_data.get_user(db, user_id=user_id)
    assert real_convs == health_datas
