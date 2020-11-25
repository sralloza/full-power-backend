from typing import Dict
from unittest import mock

from fastapi.testclient import TestClient

from app.core.config import Settings, settings

# noqa


def test_get_index(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["detail"] == "backend server online"


@mock.patch("app.api.routes.utils.__version__", "v1.0.0-testing")
def test_get_version(client: TestClient):
    response = client.get("/version")
    assert response.status_code == 200

    version = response.json()
    assert version["version"] == "v1.0.0-testing"


def test_get_settings_admin(client: TestClient, superuser_token_headers: dict):
    response = client.get("/settings", headers=superuser_token_headers)
    assert response.status_code == 200

    assert Settings.parse_obj(response.json())


def test_get_settings_normal_user(client: TestClient, normal_user_token_headers: dict):
    response = client.get("/settings", headers=normal_user_token_headers)
    assert response.status_code == 401
    assert "[admin required]" in response.json()["detail"]


def test_get_me_superuser(client: TestClient, superuser_token_headers: Dict[str, str]):
    response = client.get("/me", headers=superuser_token_headers)
    current_user = response.json()
    assert current_user
    assert current_user["id"]
    assert current_user["is_admin"]
    assert current_user["username"] == settings.first_superuser


def test_get_me_normal_user(
    client: TestClient, normal_user_token_headers: Dict[str, str]
):
    response = client.get("/me", headers=normal_user_token_headers)
    current_user = response.json()
    assert current_user
    assert current_user["id"]
    assert current_user["is_admin"] is False
    assert current_user["username"] == settings.username_test_user
