from typing import List
from unittest import mock

from fastapi.routing import APIRoute
from fastapi.testclient import TestClient

from app.main import create_app


@mock.patch("app.main.settings.production", False)
def test_docs_enabled():
    app = create_app()
    client = TestClient(app)
    docs_response = client.get("/docs")
    old_redoc_response = client.get("/redoc")
    swagger_response = client.get("/idocs")
    openapi_response = client.get("/openapi.json")

    assert docs_response.status_code == 200
    assert "redoc" in docs_response.text

    assert swagger_response.status_code == 200
    assert "swagger" in swagger_response.text

    assert old_redoc_response.status_code == 404
    assert openapi_response.status_code == 200


@mock.patch("app.main.settings.production", True)
def test_doc_disabled():
    app = create_app()
    client = TestClient(app)
    docs_response = client.get("/docs")
    old_redoc_response = client.get("/redoc")
    swagger_response = client.get("/idocs")
    openapi_response = client.get("/openapi.json")

    assert docs_response.status_code == 200
    assert "redoc" in docs_response.text

    assert swagger_response.status_code == 404

    assert old_redoc_response.status_code == 404
    assert openapi_response.status_code == 200


ignore_routes = (
    "openapi",
    "swagger_ui_html",
    "swagger_ui_redirect",
    "redoc_html",
    "static",
)


def test_routes():
    app = create_app()
    routes: List[APIRoute] = [x for x in app.routes if x.name not in ignore_routes]  # type: ignore

    for route in routes:
        assert route.summary, f"{route.name!r} must have summary"
        assert route.description, f"{route.name!r} must have description"
        assert route.tags, f"{route.name!r} must have tags"

        for tag in route.tags:
            assert tag, f"{route.name!r} tags can't be empty"
            assert tag.istitle(), f"{route.name!r} tags must be titled"

    # GET routes with parameter can raise 404
    group = [x for x in routes if "GET" in x.methods and x.param_convertors]
    for route in group:
        # notifications-content routes can't raise 404
        if "notifications-content" in route.path:
            continue
        assert 404 in route.responses, f"{route.name!r} must define 404"
        assert "not found" in route.responses[404]["description"]

    # POST routes that create objects must return 201
    group = [x for x in routes if "POST" in x.methods and x.param_convertors]
    for route in group:  # noqa
        assert route.status_code == 201

    # DELETE routes can raise 404 and must return 204
    group = [x for x in routes if "DELETE" in x.methods]
    for route in group:
        assert route.status_code == 204
        assert 404 in route.responses
        assert "not found" in route.responses[404]["description"]
