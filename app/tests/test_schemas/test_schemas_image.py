from pydantic.error_wrappers import ValidationError
from app.schemas.image import (
    ImageCreate,
    ImageCreateInner,
    ImageCreateResult,
    ImageInDB,
    ImageUpdate,
)
import pytest


def test_image_create():
    fields = ImageCreate.__fields__
    assert set(fields) == {"content"}

    assert fields["content"].required is True
    assert issubclass(fields["content"].type_, bytes)

    with pytest.raises(ValidationError):
        ImageCreate(content=b"c" * 2097153)
    ImageCreate(content=b"c" * 2097152)


def test_image_create_inner():
    fields = ImageCreateInner.__fields__
    assert set(fields) == {"content", "image_type", "mime_type"}

    assert fields["content"].required is True
    assert issubclass(fields["content"].type_, bytes)
    assert fields["image_type"].required is True
    assert fields["image_type"].type_ == str
    assert fields["mime_type"].required is True
    assert fields["mime_type"].type_ == str


def test_image_create_result():
    fields = ImageCreateResult.__fields__
    assert set(fields) == {"image_type", "mime_type", "id"}

    assert fields["image_type"].required is True
    assert fields["image_type"].type_ == str
    assert fields["mime_type"].required is True
    assert fields["mime_type"].type_ == str
    assert fields["id"].required is True
    assert fields["id"].type_ == int

    assert ImageCreateResult.__config__.orm_mode is True


def test_image_update():
    fields = ImageUpdate.__fields__
    assert set(fields) == {"content", "image_type", "mime_type"}

    assert fields["content"].required is False
    assert fields["content"].default is None
    assert issubclass(fields["content"].type_, bytes)
    assert fields["image_type"].required is False
    assert fields["image_type"].default is None
    assert fields["image_type"].type_ == str
    assert fields["mime_type"].required is False
    assert fields["mime_type"].default is None
    assert fields["mime_type"].type_ == str

    with pytest.raises(ValidationError):
        ImageCreate(content=b"c" * 2097153)
    ImageCreate(content=b"c" * 2097152)


def test_image_in_db():
    fields = ImageInDB.__fields__
    assert set(fields) == {"content", "image_type", "mime_type", "id"}

    assert fields["content"].required is True
    assert issubclass(fields["content"].type_, bytes)
    assert fields["image_type"].required is True
    assert fields["image_type"].type_ == str
    assert fields["mime_type"].required is True
    assert fields["mime_type"].type_ == str
    assert fields["id"].required is True
    assert fields["id"].type_ == int

    with pytest.raises(ValidationError):
        ImageCreate(content=b"c" * 2097153)
    ImageCreate(content=b"c" * 2097152)
    assert ImageInDB.__config__.orm_mode is True
