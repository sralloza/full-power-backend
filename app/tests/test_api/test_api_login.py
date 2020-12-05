import time
from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm.session import Session

from app import crud
from app.core.config import settings
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserCreateAdmin
from app.tests.conftest import client
from app.tests.utils.utils import random_lower_string


def test_get_access_token(client: TestClient):
    login_data = {
        "username": settings.first_superuser,
        "password": settings.first_superuser_password,
    }
    response = client.post("/login", data=login_data)
    tokens = response.json()
    assert response.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_use_access_token(client: TestClient, superuser_token_headers: Dict[str, str]):
    response = client.get("/me", headers=superuser_token_headers)
    result = response.json()
    assert response.status_code == 200
    assert "username" in result


def test_login_success(client: TestClient, db: Session):
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreateAdmin(username=username, password=password, is_admin=False)
    crud.user.create(db, obj_in=user_in)

    response = client.post("/login", data={"username": username, "password": password})
    assert response.status_code == 200
    token = Token(**response.json())
    assert token
    assert token.token_type == "Bearer"


def test_login_wrong_username(client: TestClient):
    username = random_lower_string()
    password = random_lower_string()
    response = client.post("/login", data={"username": username, "password": password})

    error = response.json()
    assert response.status_code == 401
    assert error["detail"] == "Incorrect username or password"


def test_login_wrong_password(client: TestClient, db: Session):
    username = random_lower_string()
    password = random_lower_string()
    fake_password = random_lower_string()

    user_in = UserCreateAdmin(username=username, password=password, is_admin=False)
    crud.user.create(db, obj_in=user_in)

    response = client.post(
        "/login", data={"username": username, "password": fake_password}
    )

    error = response.json()
    assert response.status_code == 401
    assert error["detail"] == "Incorrect username or password"


def test_register_basic_user(client: TestClient, db: Session):
    username = random_lower_string()
    password = random_lower_string()
    payload = {"username": username, "password": password}
    response = client.post("/register", json=payload)

    assert response.status_code == 200
    user = User(**response.json())
    assert user

    db_user = crud.user.get_by_username(db, username=username)
    assert db_user
    assert db_user.username == username
    assert user.username == username

    response_2 = client.post("/register", json=payload)
    assert response_2.status_code == 400
    assert response_2.json()["detail"] == f"User {username!r} is already registered"


def test_refresh_token(client: TestClient, normal_user_token_headers: dict):
    token1 = normal_user_token_headers["Authorization"].replace("Bearer ", "")

    time.sleep(1)
    refresh_response = client.post("/refresh", headers=normal_user_token_headers)
    assert refresh_response.status_code == 200
    token2 = refresh_response.json()["access_token"]
    assert token1 != token2

    confirm_response = client.get("/me", headers={"Authorization": f"Bearer {token2}"})
    assert confirm_response.status_code == 200
