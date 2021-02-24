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

    for route in routes:
        assert route.summary, f"{route.name!r} must have summary"  # type: ignore
        assert route.description, f"{route.name!r} must have description"  # type: ignore
        assert route.tags, f"{route.name!r} must have tags"  # type: ignore

    # GET routes with parameter can raise 404
    group = [x for x in routes if "GET" in x.methods and x.param_convertors]  # type: ignore
    for route in group:
        # notifications-content routes can't raise 404
        if "notifications-content" in route.path:  # type: ignore
            continue
        assert 404 in route.responses, f"{route.name!r} must define 404"  # type: ignore
        assert "not found" in route.responses[404]["description"]  # type: ignore

    # POST routes that create objects must return 201
    group = [x for x in routes if "POST" in x.methods and x.param_convertors]  # type: ignore
    for route in group:  # noqa
        assert route.status_code == 201  # type: ignore

    # DELETE routes can raise 404 and must return 204
    group = [x for x in routes if "DELETE" in x.methods]  # type: ignore
    for route in group:
        assert route.status_code == 204  # type: ignore
        assert 404 in route.responses  # type: ignore
        assert "not found" in route.responses[404]["description"]  # type: ignore
