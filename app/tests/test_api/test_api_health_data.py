from app.tests.utils.user import create_random_user
from typing import List

from pydantic import parse_obj_as
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app import crud
from app.schemas.health_data import HealthData
from app.tests.utils.health_data import gen_health_data_create
from app.tests.utils.utils import random_int


def test_health_data_post(client: TestClient, db: Session, superuser_token_headers):
    health_data_in = gen_health_data_create(random_int(), True)
    response = client.post(
        "/health-data", json=health_data_in.dict(), headers=superuser_token_headers
    )
    assert response.status_code == 201

    health_data_created = HealthData.parse_obj(response.json())
    assert health_data_created.id

    health_data_db = crud.health_data.get(db, id=health_data_created.id)
    assert health_data_created == HealthData.from_orm(health_data_db)


def test_health_data_get_from_user(
    client: TestClient, db: Session, superuser_token_headers: dict
):
    user_id = random_int()
    response_1 = client.get(
        f"/health-data/user/{user_id}", headers=superuser_token_headers
    )
    assert response_1.status_code == 404
    assert response_1.json()["detail"] == f"User with id={user_id} does not exist"

    user = create_random_user(db)
    user_id = user.id

    def get_health_datas():
        return gen_health_data_create(user_id, True)

    health_datas = [get_health_datas() for _ in range(7)]
    saved = []

    for health_data in health_datas:
        conv_db = crud.health_data.create(db, obj_in=health_data)
        saved.append(HealthData.from_orm(conv_db))

    response = client.get(
        f"/health-data/user/{user_id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    real_heath_datas = parse_obj_as(List[HealthData], response.json())
    assert real_heath_datas == saved


def test_get_health_data_by_id(
    client: TestClient, db: Session, superuser_token_headers
):
    user_id = random_int()
    hd_db = crud.health_data.create(db, obj_in=gen_health_data_create(user_id, True))

    response_1 = client.get(f"/health-data/{random_int()}")
    assert response_1.status_code == 401

    response_2 = client.get(
        f"/health-data/{random_int()}", headers=superuser_token_headers
    )
    assert response_2.status_code == 404

    response_3 = client.get(f"/health-data/{hd_db.id}", headers=superuser_token_headers)
    assert response_3.status_code == 200
    hd_data = HealthData(**response_3.json())
    assert hd_data == HealthData.from_orm(hd_db)


def test_health_datas_get_from_all_users(
    client: TestClient, db: Session, superuser_token_headers: dict
):
    convs_db = crud.health_data.get_multi(db)
    convs = [HealthData.from_orm(x) for x in convs_db]

    response = client.get("/health-data", headers=superuser_token_headers)
    assert response.status_code == 200
    real_heath_datas = parse_obj_as(List[HealthData], response.json())
    assert real_heath_datas == convs


def test_health_data_delete(client: TestClient, db: Session, superuser_token_headers):
    health_data_in = gen_health_data_create(random_int(), True)
    health_data_db = crud.health_data.create(db, obj_in=health_data_in)

    response = client.delete(
        f"/health-data/{health_data_db.id}", headers=superuser_token_headers
    )
    assert response.status_code == 204
    assert response.content == b""


def test_remove_nonexisting_health_data(client: TestClient, superuser_token_headers):
    response = client.delete("/health-data/84623", headers=superuser_token_headers)

    error = response.json()
    assert response.status_code == 404
    assert error["detail"] == "HealthData with id=84623 does not exist"
