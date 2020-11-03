import secrets
from datetime import timedelta
from unittest import mock

import pytest

from app import crud
from app.core.security import create_access_token
from app.tests.utils.utils import random_lower_string


@pytest.fixture
def username():
    return random_lower_string()


def get_response_from_token(client, token: str):
    headers = {"Authorization": f"Bearer {token}"}

    return client.get("/me", headers=headers)


def test_no_username_in_token(client):
    token = create_access_token({})
    response = get_response_from_token(client, token)

    assert response.status_code == 401
    assert response.headers["X-Login-Error"] == "No username in token"


def test_token_expired(client, username):
    token = create_access_token({"sub": username}, expires_delta=timedelta(days=-1))
    response = get_response_from_token(client, token)

    assert response.status_code == 401
    assert response.headers["X-Login-Error"] == "Token expired"


new_secret = secrets.token_urlsafe(32)


def test_invalid_token(client, username):
    with mock.patch("app.core.security.settings.server_secret", new_secret):
        token = create_access_token({"sub": username})

    response = get_response_from_token(client, token)

    assert response.status_code == 401
    assert response.headers["X-Login-Error"] == "Invalid token"


def test_invalid_username(client, db, username):
    assert not crud.user.get_by_username(db, username=username)
    token = create_access_token({"sub": username})
    response = get_response_from_token(client, token)

    assert response.status_code == 401
    assert response.headers["X-Login-Error"] == "Invalid username"
