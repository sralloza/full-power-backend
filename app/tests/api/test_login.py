from typing import Dict

from fastapi.testclient import TestClient

from app.core.config import settings


def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": settings.first_superuser,
        "password": settings.first_superuser_password,
    }
    r = client.post("/login", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_use_access_token(client: TestClient, superuser_token_headers: Dict[str, str]):
    r = client.get("/me", headers=superuser_token_headers)
    result = r.json()
    assert r.status_code == 200
    assert "username" in result
