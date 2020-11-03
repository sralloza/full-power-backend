import random
import string
from typing import Dict

from fastapi.testclient import TestClient

from app.core.config import settings


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_int() -> int:
    return int("".join(random.choices(string.digits, k=10)))


def get_superuser_token_headers(client: TestClient) -> Dict[str, str]:
    login_data = {
        "username": settings.first_superuser,
        "password": settings.first_superuser_password,
    }
    response = client.post("/login", data=login_data)
    tokens = response.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
