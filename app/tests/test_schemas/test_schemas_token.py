from typing import List
from unittest import mock

from app.schemas.token import Token, TokenData


def test_token_data():
    fields = TokenData.__fields__
    assert set(fields) == {"username", "scopes"}

    assert fields["username"].required is True
    assert fields["username"].type_ == str
    assert fields["scopes"].required is True
    assert fields["scopes"].outer_type_ == List[str]


@mock.patch("app.schemas.token.settings.token_expire_minutes", 654321)
def test_token():
    fields = Token.__fields__
    assert set(fields) == {"access_token", "token_type", "expires_minutes", "scopes"}

    assert fields["access_token"].required is True
    assert fields["access_token"].type_ == str
    assert fields["token_type"].required is False
    assert fields["token_type"].default == "Bearer"
    assert fields["token_type"].type_ == str
    assert fields["expires_minutes"].required is False
    assert fields["expires_minutes"].default_factory() == 654321
    assert fields["expires_minutes"].type_ == int
    assert fields["scopes"].required is True
    assert fields["scopes"].outer_type_ == List[str]
