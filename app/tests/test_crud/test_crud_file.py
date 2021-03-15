from pathlib import Path
from secrets import choice
from string import ascii_letters
from typing import List
from unittest import mock

import pytest
from fastapi import HTTPException
from pydantic import parse_file_as
from pydantic.main import BaseModel
from sqlalchemy.orm.session import Session

from app import crud
from app.core.files import get_file_id_from_name
from app.schemas.file import FileCreateInner, FileUpdate


def fci(content, name, title, lang="es"):
    file_id = get_file_id_from_name(name, lang)
    return FileCreateInner(
        content=content, id=file_id, name=name, title=title, lang=lang
    )


def test_get_db_file_list(db: Session):
    crud.file.create(db, obj_in=fci("content", "health.test.act", "a"))
    crud.file.create(db, obj_in=fci("content", "health.test.understand", "b"))
    crud.file.create(db, obj_in=fci("content", "vitamins.test", "c"))
    crud.file.create(db, obj_in=fci("content", "vitamins.not-valid", "d", "en"))

    file_list = sorted(crud.file.get_db_file_list(db, lang="es"), key=lambda x: x.name)
    assert file_list == [
        {"name": "health.test.act", "title": "a", "lang": "es"},
        {"name": "health.test.understand", "title": "b", "lang": "es"},
        {"name": "vitamins.test", "title": "c", "lang": "es"},
    ]


def test_list_files_grouped(db: Session):
    crud.file.create(db, obj_in=fci("data", "vitamins.t1", "t", "ru"))
    crud.file.create(db, obj_in=fci("data", "vitamins.t2", "t", "ru"))
    crud.file.create(db, obj_in=fci("data", "vitamins.t2", "t", "es"))

    grouped_file_list = list(crud.file.get_grouped_file_list(db))
    assert grouped_file_list == [
        {"name": "vitamins.t1", "langs": ["ru"]},
        {"name": "vitamins.t2", "langs": ["es", "ru"]},
    ]


def test_get_or_404(db: Session):
    with pytest.raises(HTTPException) as exc:
        crud.file.get_or_404_by_name(db, name="health.something.act", lang="es")
    assert exc.value.status_code == 404
    detail = "File with name=health.something.act and lang=es does not exist"
    assert exc.value.detail == detail

    crud.file.create(db, obj_in=fci("content", "health.something.act", "a"))
    result = crud.file.get_or_404_by_name(db, name="health.something.act", lang="es")

    assert result.name == "health.something.act"
    assert result.lang == "es"
    assert result.title == "a"
    assert result.content == "content"


@mock.patch("app.crud.file.autoremove_images")
def test_create(ari_m, db: Session):
    file_db = crud.file.create(db, obj_in=fci("content", "vitamins.calcium", "k"))
    expected_dict = {
        "content": "content",
        "id": mock.ANY,
        "lang": "es",
        "name": "vitamins.calcium",
        "title": "k",
    }
    assert file_db.dict() == expected_dict
    assert file_db == crud.file.get_by_name(db, name="vitamins.calcium", lang="es")

    ari_m.assert_called_once()


def test_create_already_exists(db: Session):
    crud.file.create(db, obj_in=fci("content", "vitamins.k", "p", "pr"))
    crud.file.create(db, obj_in=fci("content", "vitamins.k", "u", "en"))

    with pytest.raises(HTTPException) as exc:
        crud.file.create(db, obj_in=fci("content", "vitamins.k", "d", "en"))

    assert exc.value.status_code == 409
    assert exc.value.detail == "File with name=vitamins.k and lang=en already exists"


@mock.patch("app.crud.file.autoremove_images")
def test_update(ari_m, db: Session):
    file_db = crud.file.create(db, obj_in=fci("content", "vitamins.qwerty", "r"))
    assert file_db.content == "content"
    assert file_db.name == "vitamins.qwerty"
    assert file_db.lang == "es"
    assert file_db.title == "r"

    ari_m.reset_mock()

    # Update only content and title
    file_db_2 = crud.file.update(
        db, db_obj=file_db, obj_in=FileUpdate(content="new-content", title="x")
    )
    assert file_db_2.content == "new-content"
    assert file_db_2.name == "vitamins.qwerty"
    assert file_db_2.lang == "es"
    assert file_db_2.title == "x"
    assert file_db == file_db_2
    ari_m.assert_called_once()
    ari_m.reset_mock()

    # Update lang and name
    file_db_2 = crud.file.update(
        db, db_obj=file_db, obj_in=FileUpdate(name="vitamins.asdf", lang="ru")
    )
    assert file_db_2.content == "new-content"
    assert file_db_2.name == "vitamins.asdf"
    assert file_db_2.lang == "ru"
    assert file_db_2.title == "x"
    assert file_db == file_db_2
    ari_m.assert_called_once()


@mock.patch("app.crud.file.autoremove_images")
def test_remove(ari_m, db: Session):
    file_db = crud.file.create(db, obj_in=fci("content", "vitamins.gh", "q", "pt"))
    assert file_db == crud.file.get_by_name(db, name="vitamins.gh", lang="pt")
    ari_m.reset_mock()

    result = crud.file.remove(db, id=get_file_id_from_name("vitamins.gh", "pt"))
    assert result is None

    assert crud.file.get(db, id=get_file_id_from_name("vitamins.gh", "pt")) is None
    ari_m.assert_called_once()


class ARITestData(BaseModel):
    files: List[str]
    images: List[int]
    remove: List[int]


ari_test_data_path = Path(__file__).parent.parent / "test_data/autoremove_images.json"
ari_test_data = parse_file_as(List[ARITestData], ari_test_data_path)


@pytest.mark.parametrize("test_data", ari_test_data)
@mock.patch("app.crud.image.get_id_list")
@mock.patch("app.crud.image.remove")
def test_autoremove_images(remove_image_m, gil_m, db: Session, test_data: ARITestData):
    gil_m.return_value = test_data.images

    for content in test_data.files:
        name = "vitamins." + choice(ascii_letters)
        file = fci(content, name, "title")
        crud.file.create(db, obj_in=file)

    remove_image_m.reset_mock()
    gil_m.reset_mock()

    crud.file.autoremove_images(db)

    calls = [mock.call(db, id=x) for x in test_data.remove]
    remove_image_m.assert_has_calls(calls, any_order=True)
    assert remove_image_m.call_count == len(calls)

    gil_m.assert_called_once()
