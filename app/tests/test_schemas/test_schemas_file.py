import pytest
from pydantic import ValidationError

from app.schemas.file import (
    FileBase,
    FileCreate,
    FileCreateInner,
    FileCreateResult,
    FileDelete,
    FileInDB,
    FileResult,
    FileUpdate,
    FileUpdateInner,
)

invalid_name_test_data = (
    ("invalid-key", "Must contain at least one dot"),
    ("invalid.key", "Primary key must be 'health' or 'vitamines'"),
    ("vitamins.invalid.key", "Vitamin's secondary key can't contain dots"),
    ("health.invalid", "Health's secondary key must contain excactly one dot"),
    ("health.invalid.key", "Health type must be 'act' or 'understand'"),
    ("health.some.invalid.key", "Health's secondary key must contain excactly one dot"),
    ("health.some.invalid.act", "Health's secondary key must contain excactly one dot"),
    (
        "health.some.invalid.understand",
        "Health's secondary key must contain excactly one dot",
    ),
)


@pytest.mark.parametrize("name,match", invalid_name_test_data)
def test_name_validator_invalid(name, match):
    with pytest.raises(ValidationError, match=match):
        FileBase(name=name)


valid_ids = (
    "health.key.act",
    "health.key.understand",
    "vitamins.a",
    "vitamins.calcium",
    "vitamins.h2o",
)


@pytest.mark.parametrize("name", valid_ids)
def test_name_validator_valid(name):
    FileBase(name=name)


def test_file_create():
    fields = FileCreate.__fields__

    assert set(fields) == {"name", "content", "title"}
    assert fields["name"].required is True
    assert fields["name"].type_ == str
    assert fields["content"].required is True
    assert fields["content"].type_ == str
    assert fields["title"].required is True
    assert fields["title"].type_ == str


def test_file_create_inner():
    fields = FileCreateInner.__fields__

    assert set(fields) == {"name", "content", "title", "id", "lang"}
    assert fields["name"].required is True
    assert fields["name"].type_ == str
    assert fields["content"].required is True
    assert fields["content"].type_ == str
    assert fields["title"].required is True
    assert fields["title"].type_ == str
    assert fields["id"].required is True
    assert fields["id"].type_ == str
    assert fields["lang"].required is True
    assert fields["lang"].type_ == str


def test_file_create_result():
    fields = FileCreateResult.__fields__

    assert set(fields) == {"name", "title", "lang"}
    assert fields["name"].required is True
    assert fields["name"].type_ == str
    assert fields["title"].required is True
    assert fields["title"].type_ == str
    assert fields["lang"].required is True
    assert fields["lang"].type_ == str

    assert FileCreateResult.__config__.orm_mode is True


def test_file_update():
    fields = FileUpdate.__fields__

    assert set(fields) == {"name", "content", "title", "lang"}
    assert fields["name"].required is False
    assert fields["name"].type_ == str
    assert fields["content"].required is False
    assert fields["content"].type_ == str
    assert fields["title"].required is False
    assert fields["title"].type_ == str
    assert fields["lang"].required is False
    assert fields["lang"].type_ == str


def test_file_update_inner():
    fields = FileUpdateInner.__fields__

    assert set(fields) == {"name", "content", "title", "lang", "id"}
    assert fields["name"].required is False
    assert fields["name"].type_ == str
    assert fields["content"].required is False
    assert fields["content"].type_ == str
    assert fields["title"].required is False
    assert fields["title"].type_ == str
    assert fields["lang"].required is False
    assert fields["lang"].type_ == str
    assert fields["id"].required is False
    assert fields["id"].type_ == str


def test_file_in_db():
    fields = FileInDB.__fields__

    assert set(fields) == {"name", "content", "lang", "title", "id"}
    assert fields["name"].required is True
    assert fields["name"].type_ == str
    assert fields["content"].required is True
    assert fields["content"].type_ == str
    assert fields["lang"].required is True
    assert fields["lang"].type_ == str
    assert fields["title"].required is True
    assert fields["title"].type_ == str
    assert fields["id"].required is True
    assert fields["id"].type_ == str

    assert FileInDB.__config__.orm_mode is True


def test_file_result():
    fields = FileResult.__fields__

    assert set(fields) == {"name", "title", "lang", "content"}
    assert fields["name"].required is True
    assert fields["name"].type_ == str
    assert fields["title"].required is True
    assert fields["title"].type_ == str
    assert fields["lang"].required is True
    assert fields["lang"].type_ == str
    assert fields["content"].required is True
    assert fields["content"].type_ == str

    assert FileCreateResult.__config__.orm_mode is True


def test_file_delete():
    fields = FileDelete.__fields__

    assert set(fields) == {"name", "lang"}
    assert fields["name"].required is True
    assert fields["name"].type_ == str
    assert fields["lang"].required is True
    assert fields["lang"].type_ == str

    assert FileCreateResult.__config__.orm_mode is True
