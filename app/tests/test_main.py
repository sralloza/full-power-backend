from inspect import signature
from operator import attrgetter
from typing import List
from unittest import mock

import pytest
from fastapi.params import Depends, Security
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


def is_public(route: APIRoute) -> bool:
    if route.name == "login":
        return True
    if requires_admin(route):
        return False
    return not requires_normal_user(route)


def requires_normal_user(route: APIRoute) -> bool:
    if requires_admin(route):
        return False
    for dependency in route.dependencies:
        if isinstance(dependency, Depends) and dependency.dependency:  # noqa
            if dependency.dependency.__name__ == "get_current_user":
                return True

    for argument in signature(route.endpoint).parameters.values():
        dependency = argument.default
        if isinstance(dependency, Depends) and dependency.dependency:
            if dependency.dependency.__name__ == "get_current_user":
                return True
    return False


def requires_admin(route: APIRoute) -> bool:
    for dependency in route.dependencies:
        if isinstance(dependency, Security) and dependency.dependency:  # noqa
            if "admin" in dependency.scopes:
                return True

    for argument in signature(route.endpoint).parameters.values():  # noqa
        dependency = argument.default
        if isinstance(dependency, Security) and dependency.dependency:
            if "admin" in dependency.scopes:
                return True

    return False


def creates_object(route: APIRoute):
    if "POST" not in route.methods:
        return False
    return "create" in route.name or route.name == "register_basic_user"


class TestRoutesDocs:
    app = create_app()
    routes: List[APIRoute] = [x for x in app.routes if x.name not in ignore_routes]  # type: ignore
    asdf = {x.name: x.param_convertors for x in routes}
    get_group = [x for x in routes if "GET" in x.methods and x.param_convertors]
    create_group = [x for x in routes if creates_object(x)]
    delete_group = [x for x in routes if "DELETE" in x.methods]
    admin_group = [x for x in routes if requires_admin(x)]
    user_group = [x for x in routes if requires_normal_user(x)]
    public_group = [x for x in routes if is_public(x)]
    id_generator = attrgetter("name")

    @pytest.mark.parametrize("route", routes, ids=id_generator)
    def test_general(self, route: APIRoute):
        assert route.summary, f"{route.name!r} must have summary"
        assert route.description, f"{route.name!r} must have description"
        assert route.tags, f"{route.name!r} must have tags"

        for tag in route.tags:
            assert tag, f"{route.name!r} tags can't be empty"
            assert tag.istitle(), f"{route.name!r} tags must be titled"

    @pytest.mark.parametrize("route", get_group, ids=id_generator)
    def test_get_404(self, route: APIRoute):
        # GET routes with parameter can raise 404
        # notifications-content routes can't raise 404
        if "notifications-content" in route.path:
            return
        assert 404 in route.responses, f"{route.name!r} must define 404"
        assert "not found" in route.responses[404]["description"]

    @pytest.mark.parametrize("route", create_group, ids=id_generator)
    def test_post_201(self, route: APIRoute):
        # POST routes that create objects must return 201
        assert route.status_code == 201

    @pytest.mark.parametrize("route", delete_group, ids=id_generator)
    def test_delete_401_204(self, route: APIRoute):
        # DELETE routes can raise 404 and must return 204
        assert route.status_code == 204
        assert 404 in route.responses, f"{route.name!r} must define 404"
        assert "not found" in route.responses[404]["description"]

    @pytest.mark.parametrize("route", user_group, ids=id_generator)
    def test_user_401(self, route: APIRoute):
        assert 401 in route.responses, f"{route.name!r} must define 401 (user)"
        assert route.responses[401]["description"] == "User not logged in"

    @pytest.mark.parametrize("route", admin_group, ids=id_generator)
    def test_admin_401(self, route: APIRoute):
        assert 403 in route.responses, f"{route.name!r} must define 401 (admin)"
        assert route.responses[403]["description"] == "Admin access required"

    @pytest.mark.parametrize("route", public_group, ids=id_generator)
    def test_not_401_or_403(self, route: APIRoute):
        if route.name == "login":
            return
        msg = f"{route.name!r} must not define 401 or 403 (public)"
        assert 401 not in route.responses, msg
        assert 403 not in route.responses, msg
