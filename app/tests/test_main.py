from unittest import mock

from fastapi.testclient import TestClient

from app.main import create_app


@mock.patch("app.main.settings.production", False)
def test_docs_enabled():
    app = create_app()
    client = TestClient(app)
    response_1 = client.get("/docs")
    response_2 = client.get("/redoc")
    response_3 = client.get("/openapi.json")

    assert response_1.status_code == 200
    assert response_2.status_code == 200
    assert response_3.status_code == 200


@mock.patch("app.main.settings.production", True)
def test_doc_disabled():
    app = create_app()
    client = TestClient(app)
    response_1 = client.get("/docs")
    response_2 = client.get("/redoc")
    response_3 = client.get("/openapi.json")

    assert response_1.status_code == 404
    assert response_2.status_code == 404
    assert response_3.status_code == 404
