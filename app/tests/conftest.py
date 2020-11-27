import os
from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient

from app import app
from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.tests.utils.user import (
    create_test_user,
    get_normal_user_token_headers,
    get_superuser_token_headers,
)


@pytest.fixture(scope="session")
def db() -> Generator:
    db = SessionLocal()
    init_db(db)
    create_test_user(db)
    yield db
    db.close()
    os.remove("testing-database.db")


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> Dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient) -> Dict[str, str]:
    return get_normal_user_token_headers(client)
