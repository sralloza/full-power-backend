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


ignore_routes = (
    "openapi",
    "swagger_ui_html",
    "swagger_ui_redirect",
    "redoc_html",
    "static",
)


def test_routes():
    app = create_app()
    routes = [x for x in app.routes if x.name not in ignore_routes]  # type: ignore

    no_summary = [x for x in routes if not hasattr(x, "summary")]
    assert len(no_summary) == 0

    no_description = [x for x in routes if not hasattr(x, "description")]
    assert len(no_description) == 0

    no_tags = [x for x in routes if not hasattr(x, "tags")]
    assert len(no_tags) == 0

    # GET routes with parameter can raise 404
    group = [x for x in routes if "GET" in x.methods and x.param_convertors]  # type: ignore
    for route in group:
        assert 404 in route.responses  # type: ignore
        assert "not found" in route.responses[404]["description"]  # type: ignore

    # POST routes that create objects must return 201
    group = [x for x in routes if "POST" in x.methods and x.param_convertors]  # type: ignore
    for route in group:
        assert route.status_code == 201  # type: ignore

    # DELETE routes can raise 404 and must return 204
    group = [x for x in routes if "DELETE" in x.methods]  # type: ignore
    for route in group:
        assert route.status_code == 204  # type: ignore
        assert 404 in route.responses  # type: ignore
        assert "not found" in route.responses[404]["description"]  # type: ignore
