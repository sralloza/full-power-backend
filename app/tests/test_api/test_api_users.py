from typing import Set

from fastapi.testclient import TestClient
from pydantic import parse_obj_as
from sqlalchemy.orm import Session

from app import crud
from app.schemas.user import UserCreateAdmin, UserInDB
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
    assert "[admin access required]" in response.json()["detail"]


def test_create_user_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
):
    username = random_lower_string()
    password = random_lower_string()
    data = {"username": username, "password": password, "is_admin": False}
    response = client.post(
        "/users",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 201
    created_user = response.json()
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

    response = client.post(
        "/users", headers=superuser_token_headers, json=user_in.dict()
    )
    assert response.status_code == 409
    assert response.json()["detail"] == f"User {username!r} is already registered"


def test_get_existing_user(
    client: TestClient, superuser_token_headers: dict, db: Session
):
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreateAdmin(username=username, password=password, is_admin=False)
    user = crud.user.create(db, obj_in=user_in)

    response = client.get(f"/users/{user.id}", headers=superuser_token_headers)
    assert response.status_code == 200

    api_user = response.json()
    existing_user = crud.user.get_by_username(db, username=username)
    assert existing_user
    assert existing_user.username == api_user["username"]


def test_get_nonexisting_user(client: TestClient, superuser_token_headers: dict):
    response = client.get("/users/165468321231323", headers=superuser_token_headers)
    assert response.status_code == 404

    error = response.json()
    assert error["detail"] == "User with id=165468321231323 does not exist"


def test_retrieve_users(client: TestClient, superuser_token_headers: dict, db: Session):
    username_1 = random_lower_string()
    password_2 = random_lower_string()
    user_in_1 = UserCreateAdmin(
        username=username_1, password=password_2, is_admin=False
    )
    user_db_1 = crud.user.create(db, obj_in=user_in_1)

    username_2 = random_lower_string()
    password_2 = random_lower_string()
    user_in_2 = UserCreateAdmin(
        username=username_2, password=password_2, is_admin=False
    )
    user_db_2 = crud.user.create(db, obj_in=user_in_2)

    users = {UserInDB.from_orm(x) for x in [user_db_1, user_db_2]}

    response = client.get("/users", headers=superuser_token_headers)
    assert response.status_code == 200
    all_users = parse_obj_as(Set[UserInDB], response.json())

    assert users.issubset(all_users)


def test_remove_existing_user(
    client: TestClient, superuser_token_headers: dict, db: Session
):
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreateAdmin(username=username, password=password, is_admin=False)
    user = crud.user.create(db, obj_in=user_in)

    response = client.delete(f"/users/{user.id}", headers=superuser_token_headers)
    assert response.status_code == 204

    assert response.content == b""
    assert crud.user.get_by_username(db, username=username) is None


def test_remove_nonexisting_user(
    client: TestClient, superuser_token_headers: dict, db: Session
):
    response = client.delete("/users/46549812123", headers=superuser_token_headers)
    assert response.status_code == 404

    error = response.json()
    assert error["detail"] == "User with id=46549812123 does not exist"
