from datetime import datetime
from typing import List

from app.schemas.conversation import Conversation
from app.schemas.user import (
    UserCreateAdmin,
    UserCreateAdminInner,
    UserCreateBasic,
    UserInDB,
    UserPublic,
    UserUpdateAdmin,
    UserUpdateBasic,
    UserUpdateInner,
)


def test_user_create_basic():
    fields = UserCreateBasic.__fields__
    assert set(fields.keys()) == {"username", "password"}

    assert fields["username"].required is True
    assert fields["username"].type_ == str
    assert fields["password"].required is True
    assert fields["password"].type_ == str


def test_user_create_admin():
    fields = UserCreateAdmin.__fields__
    assert set(fields.keys()) == {"username", "password", "is_admin"}

    assert fields["username"].required is True
    assert fields["username"].type_ == str
    assert fields["password"].required is True
    assert fields["password"].type_ == str
    assert fields["is_admin"].required is False
    assert fields["is_admin"].default is False
    assert fields["is_admin"].type_ == bool


def test_user_create_admin_inner():
    fields = UserCreateAdminInner.__fields__
    assert set(fields.keys()) == {"username", "is_admin", "hashed_password"}

    assert fields["username"].required is True
    assert fields["username"].type_ == str
    assert fields["hashed_password"].required is True
    assert fields["hashed_password"].type_ == str
    assert fields["is_admin"].required is False
    assert fields["is_admin"].default is False
    assert fields["is_admin"].type_ == bool


def test_user_update_basic():
    fields = UserUpdateBasic.__fields__
    assert set(fields.keys()) == {"username", "password"}

    assert fields["username"].required is False
    assert fields["username"].type_ == str
    assert fields["password"].required is False
    assert fields["password"].type_ == str


def test_user_update_admin():
    fields = UserUpdateAdmin.__fields__
    assert set(fields.keys()) == {"username", "password", "is_admin"}

    assert fields["username"].required is False
    assert fields["username"].type_ == str
    assert fields["password"].required is False
    assert fields["password"].type_ == str
    assert fields["is_admin"].required is False
    assert fields["is_admin"].type_ == bool


def test_user_update_inner():
    fields = UserUpdateInner.__fields__
    assert set(fields.keys()) == {"username", "is_admin", "hashed_password"}

    assert fields["username"].required is False
    assert fields["username"].type_ == str
    assert fields["hashed_password"].required is False
    assert fields["hashed_password"].type_ == str
    assert fields["is_admin"].required is False
    assert fields["is_admin"].type_ == bool


def test_user_in_db():
    fields = UserInDB.__fields__
    assert set(fields.keys()) == {
        "username",
        "id",
        "is_admin",
        # "conversations",
        "last_login",
        "hashed_password",
    }

    assert fields["username"].required is True
    assert fields["username"].type_ == str
    assert fields["id"].required is True
    assert fields["id"].type_ == int
    assert fields["is_admin"].required is True
    assert fields["is_admin"].type_ == bool
    # assert fields["conversations"].required is True
    # assert fields["conversations"].outer_type_ == List[Conversation]
    assert fields["last_login"].required is True
    assert fields["last_login"].type_ == datetime
    assert fields["hashed_password"].required is True
    assert fields["hashed_password"].type_ == str

    assert UserInDB.__config__.orm_mode is True


def test_user_public():
    fields = UserPublic.__fields__
    assert set(fields.keys()) == {"username", "is_admin"}

    assert fields["username"].required is True
    assert fields["username"].type_ == str
    assert fields["is_admin"].required is True
    assert fields["is_admin"].type_ == bool

    assert UserInDB.__config__.orm_mode is True
