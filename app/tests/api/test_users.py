from typing import List

from fastapi.testclient import TestClient
from pydantic import parse_obj_as
from sqlalchemy.orm import Session

from app import crud
from app.schemas.user import User, UserCreateAdmin
from app.tests.utils.utils import random_lower_string


def test_create_user_normal_user(client: TestClient, normal_user_token_headers: dict):
    username = random_lower_string()
    password = random_lower_string()
    data = {"email": username, "password": password}
    response = client.post(
        "/users",
        headers=normal_user_token_headers,
        json=data,
    )

    assert response.status_code == 401
    assert "[admin required]" in response.json()["detail"]


def test_create_user_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
):
    username = random_lower_string()
    password = random_lower_string()
    data = {"username": username, "password": password, "is_admin": False}
    r = client.post(
        "/users",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 200
    created_user = r.json()
    user = crud.user.get_by_username(db, username=username)
    assert user
    assert user.username == created_user["username"]


def test_create_user_existing_username(
    client: TestClient, superuser_token_headers: dict, db: Session
):
    username = random_lower_string()
    password = random_lower_string()

    user_in = UserCreateAdmin(username=username, password=password, is_admin=False)
    crud.user.create(db, obj_in=user_in)

    r = client.post("/users", headers=superuser_token_headers, json=user_in.dict())
    assert r.status_code == 400
    assert r.json()["detail"] == "Username already registered"


def test_get_existing_user(
    client: TestClient, superuser_token_headers: dict, db: Session
):
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreateAdmin(username=username, password=password, is_admin=False)
    user = crud.user.create(db, obj_in=user_in)

    r = client.get(f"/users/{user.id}", headers=superuser_token_headers)
    assert r.status_code == 200

    api_user = r.json()
    existing_user = crud.user.get_by_username(db, username=username)
    assert existing_user
    assert existing_user.username == api_user["username"]


def test_get_nonexisting_user(client: TestClient, superuser_token_headers: dict):
    r = client.get(f"/users/165468321231323", headers=superuser_token_headers)
    assert r.status_code == 404

    error = r.json()
    assert error["detail"] == "User not found"


def test_retrieve_users(client: TestClient, superuser_token_headers: dict, db: Session):
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreateAdmin(username=username, password=password, is_admin=False)
    crud.user.create(db, obj_in=user_in)

    username2 = random_lower_string()
    password2 = random_lower_string()
    user_in2 = UserCreateAdmin(username=username2, password=password2, is_admin=False)
    crud.user.create(db, obj_in=user_in2)

    r = client.get("/users", headers=superuser_token_headers)
    all_users = r.json()

    assert len(all_users) > 1
    assert parse_obj_as(List[User], all_users)


def test_remove_existing_user(
    client: TestClient, superuser_token_headers: dict, db: Session
):
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreateAdmin(username=username, password=password, is_admin=False)
    user = crud.user.create(db, obj_in=user_in)

    r = client.delete(f"/users/{user.id}", headers=superuser_token_headers)
    assert r.status_code == 200

    assert r.json() is None
    assert crud.user.get_by_username(db, username=username) is None

def test_remove_nonexisting_user(
    client: TestClient, superuser_token_headers: dict, db: Session
):
    r = client.delete(f"/users/46549812123", headers=superuser_token_headers)
    assert r.status_code == 404

    error = r.json()
    assert error["detail"] == "User not found"
