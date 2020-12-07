from unittest import mock

import pytest
from fastapi import HTTPException

from app import crud, models
from app.schemas.image import ImageCreate, ImageCreateInner, ImageUpdate
from app.tests.utils.utils import random_bytes


def simulation_image_process(image_content):
    return ImageCreateInner(
        content=image_content,
        image_type="image-type-processed",
        mime_type="mime-type-processed",
    )


@mock.patch("app.crud.crud_image.process_image_content")
def test_get_or_404(pic_m, db):
    content = random_bytes()
    pic_m.side_effect = simulation_image_process

    with pytest.raises(HTTPException) as exc:
        crud.image.get_or_404(db, id=9840948)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Image with id=9840948 does not exist"

    image_in = ImageCreate(content=content)
    image_db_1 = crud.image.create(db, obj_in=image_in)
    image_db_2 = crud.image.get_or_404(db, id=image_db_1.id)
    assert image_db_1 == image_db_2


@mock.patch("app.crud.crud_image.process_image_content")
def test_get_id_list(pic_m, db):
    pic_m.side_effect = simulation_image_process

    image_db_1 = crud.image.create(db, obj_in=ImageCreate(content=b"useless"))
    image_db_2 = crud.image.create(db, obj_in=ImageCreate(content=b"useless"))
    image_db_3 = crud.image.create(db, obj_in=ImageCreate(content=b"useless"))

    ids = [image_db_1.id, image_db_2.id, image_db_3.id]
    assert ids == list(crud.image.get_id_list(db))


@mock.patch("app.crud.crud_image.process_image_content")
def test_create(pic_m, db):
    content = random_bytes()
    pic_m.side_effect = simulation_image_process
    real_image_in = simulation_image_process(content)

    image_in = ImageCreate(content=content)
    image_db = crud.image.create(db, obj_in=image_in)

    assert real_image_in.content == image_in.content
    assert real_image_in.content == image_db.content
    assert real_image_in.image_type == image_db.image_type
    assert real_image_in.mime_type == image_db.mime_type
    assert image_db.id


@mock.patch("app.crud.crud_image.process_image_content")
def test_update(pic_m, db):
    content = random_bytes()
    pic_m.side_effect = simulation_image_process
    real_image_in = simulation_image_process(content)

    image_in = ImageCreate(content=content)
    image_db = crud.image.create(db, obj_in=image_in)

    assert content == image_in.content == real_image_in.content
    assert real_image_in.image_type == image_db.image_type
    assert real_image_in.mime_type == image_db.mime_type

    image_db_2 = crud.image.update(
        db, db_obj=image_db, obj_in=ImageUpdate(image_type="image-type")
    )
    assert image_db_2.content == content
    assert image_db_2 == crud.image.get(db, id=image_db.id)
    assert image_db_2.image_type == "image-type"
    assert image_db_2.mime_type == real_image_in.mime_type

    image_db_3 = crud.image.update(
        db, db_obj=image_db, obj_in=ImageUpdate(mime_type="mime-type")
    )
    assert image_db_3 == crud.image.get(db, id=image_db.id)
    assert image_db_3.image_type == "image-type"
    assert image_db_3.mime_type == "mime-type"

    new_content = random_bytes()
    new_real_image_in = simulation_image_process(new_content)
    image_db_4 = crud.image.update(
        db,
        db_obj=image_db,
        obj_in=ImageUpdate(
            content=new_content, image_type="ignored", mime_type="ignored"
        ),
    )
    assert image_db_4 == crud.image.get(db, id=image_db.id)
    assert image_db_4.image_type == new_real_image_in.image_type
    assert image_db_4.mime_type == new_real_image_in.mime_type

    assert image_db == image_db_2 == image_db_3 == image_db_4


@mock.patch("app.crud.crud_image.process_image_content")
def test_remove(pic_m, db):
    content = random_bytes()
    pic_m.side_effect = simulation_image_process

    image_in = ImageCreate(content=content)
    image_db = crud.image.create(db, obj_in=image_in)
    assert image_db == crud.image.get(db, id=image_db.id)

    result = crud.image.remove(db, id=image_db.id)
    assert result is None

    with pytest.raises(HTTPException) as exc:
        crud.image.get_or_404(db, id=image_db.id)

    assert exc.value.status_code == 404
    assert exc.value.detail == f"Image with id={image_db.id} does not exist"
