# crud.file.remove(db, id=file_id)

from unittest import mock

import pytest
from fastapi import HTTPException
from sqlalchemy.orm.session import Session

from app import crud, models
from app.core.files import get_file_id_from_name
from app.schemas.file import FileCreateInner, FileUpdate


def fci(content, name, title, lang="es"):
    file_id = get_file_id_from_name(name, lang)
    return FileCreateInner(
        content=content, id=file_id, name=name, title=title, lang=lang
    )


def test_get_db_file_list(db: Session):
    # First we remove all data
    file_ids = [x[0] for x in db.query(models.File.id).all()]
    for file_id in file_ids:  # noqa
        crud.file.remove(db, id=file_id)

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


def test_get_or_404(db: Session):
    # First we remove all data
    file_ids = [x[0] for x in db.query(models.File.id).all()]
    for file_id in file_ids:
        crud.file.remove(db, id=file_id)

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


def test_create(db: Session):
    file_db = crud.file.create(db, obj_in=fci("content", "vitamins.calcium", "k"))
    expected_dict = {
        "content": "content",
        "id": mock.ANY,
        "lang": "es",
        "name": "vitamins.calcium",
        "title": "k",
    }
    assert file_db.dict() == expected_dict  # type: ignore
    assert file_db == crud.file.get_by_name(db, name="vitamins.calcium", lang="es")


def test_create_already_exists(db: Session):
    crud.file.create(db, obj_in=fci("content", "vitamins.k", "p", "pr"))
    crud.file.create(db, obj_in=fci("content", "vitamins.k", "u", "en"))

    with pytest.raises(HTTPException) as exc:
        crud.file.create(db, obj_in=fci("content", "vitamins.k", "d", "en"))

    assert exc.value.status_code == 400
    assert exc.value.detail == "File with name=vitamins.k and lang=en already exists"


def test_update(db: Session):
    file_db = crud.file.create(db, obj_in=fci("content", "vitamins.qwerty", "r"))
    assert file_db.content == "content"
    assert file_db.name == "vitamins.qwerty"
    assert file_db.lang == "es"
    assert file_db.title == "r"

    # Update only content and title
    file_db_2 = crud.file.update(
        db, db_obj=file_db, obj_in=FileUpdate(content="new-content", title="x")
    )
    assert file_db_2.content == "new-content"
    assert file_db_2.name == "vitamins.qwerty"
    assert file_db_2.lang == "es"
    assert file_db_2.title == "x"
    assert file_db == file_db_2

    # Update lang and name
    file_db_2 = crud.file.update(
        db, db_obj=file_db, obj_in=FileUpdate(name="vitamins.asdf", lang="ru")
    )
    assert file_db_2.content == "new-content"
    assert file_db_2.name == "vitamins.asdf"
    assert file_db_2.lang == "ru"
    assert file_db_2.title == "x"
    assert file_db == file_db_2


def test_remove(db: Session):
    file_db = crud.file.create(db, obj_in=fci("content", "vitamins.gh", "q", "pt"))
    assert file_db == crud.file.get_by_name(db, name="vitamins.gh", lang="pt")
    result = crud.file.remove(db, id=get_file_id_from_name("vitamins.gh", "pt"))
    assert result is None

    assert crud.file.get(db, id=get_file_id_from_name("vitamins.gh", "pt")) is None
