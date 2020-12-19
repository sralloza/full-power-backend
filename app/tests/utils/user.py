from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreateAdmin, UserUpdateAdmin
from app.tests.utils.utils import random_lower_string

temp_passwords = {}


def user_authentication_headers(
    *, client: TestClient, username: str, password: str
) -> Dict[str, str]:
    data = {"username": username, "password": password}

    reponse = client.post("/login", data=data)
    response = reponse.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def create_random_user(db: Session, username: str = None, password: str = None) -> User:
    username = username or random_lower_string()
    password = password or random_lower_string()
    user_in = UserCreateAdmin(username=username, password=password, is_admin=False)
    user = crud.user.create(db=db, obj_in=user_in)
    return user


def authentication_token_from_username(
    *, client: TestClient, username: str, db: Session
) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.
    If the user doesn't exist it is created first.
    """
    user = crud.user.get_by_username(db, username=username)

    if username not in temp_passwords:
        temp_passwords[username] = random_lower_string()

        if not user:
            user_in_create = UserCreateAdmin(
                username=username, password=temp_passwords[username], is_admin=False
            )
            user = crud.user.create(db, obj_in=user_in_create)
        else:
            user_in_update = UserUpdateAdmin(
                username=username, password=temp_passwords[username]
            )
            user = crud.user.update(db, db_obj=user, obj_in=user_in_update)

    password = temp_passwords[username]
    return user_authentication_headers(
        client=client, username=username, password=password
    )


def create_test_user(db: Session):
    user_in = UserCreateAdmin(
        username=settings.username_test_user,
        password=settings.username_test_password,
        is_admin=False,
    )
    user_db = crud.user.get_by_username(db, username=user_in.username)
    if not user_db:
        user = crud.user.create(db=db, obj_in=user_in)
        return user
    return user_db


def get_superuser_token_headers(client: TestClient) -> Dict[str, str]:
    from .user import user_authentication_headers

    return user_authentication_headers(
        client=client,
        username=settings.first_superuser,
        password=settings.first_superuser_password,
    )


def get_normal_user_token_headers(client: TestClient) -> Dict[str, str]:
    from .user import user_authentication_headers

    return user_authentication_headers(
        client=client,
        username=settings.username_test_user,
        password=settings.username_test_password,
    )


def get_normal_user_id(db: Session) -> int:
    return crud.user.get_by_username(db, username=settings.username_test_user).id
