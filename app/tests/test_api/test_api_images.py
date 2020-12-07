from unittest import mock

from fastapi.testclient import TestClient
from sqlalchemy.orm.session import Session

from app import crud, models
from app.schemas.image import ImageCreate, ImageCreateInner, ImageCreateResult


def simulation_image_process(image_content):
    return ImageCreateInner(
        content=image_content,
        image_type="image-type-processed",
        mime_type="mime-type-processed",
    )


@mock.patch("app.crud.crud_image.process_image_content")
def test_get_image(pic_m, client: TestClient, db: Session):
    pic_m.side_effect = simulation_image_process
    image_db = crud.image.create(db, obj_in=ImageCreate(content=b"invalid"))

    response = client.get("/images/%d" % image_db.id)
    assert response.status_code == 200
    assert response.headers["content-type"] == "mime-type-processed"
    assert response.content == b"invalid"


@mock.patch("app.crud.crud_image.process_image_content")
def test_get_image_id_list(pic_m, client: TestClient, db: Session):
    pic_m.side_effect = simulation_image_process

    ids = []
    for _ in range(10):
        ids.append(crud.image.create(db, obj_in=ImageCreate(content=b"invalid")).id)

    response = client.get("/images")
    assert response.status_code == 200
    assert response.json() == ids


@mock.patch("app.crud.crud_image.process_image_content")
def test_create_image(pic_m, client: TestClient, db: Session, superuser_token_headers):
    pic_m.side_effect = simulation_image_process
    file = {"image_content": ("image.png", b"image-binary")}

    response_1 = client.post("/images", files=file)
    assert response_1.status_code == 401

    response_2 = client.post("/images", files=file, headers=superuser_token_headers)
    assert response_2.status_code == 200

    image_result = ImageCreateResult(**response_2.json())
    assert image_result.dict() == response_2.json()


@mock.patch("app.crud.crud_image.process_image_content")
def test_remove_image_list(
    pic_m, client: TestClient, db: Session, superuser_token_headers
):
    pic_m.side_effect = simulation_image_process

    ids = []
    for _ in range(10):
        ids.append(crud.image.create(db, obj_in=ImageCreate(content=b"invalid")).id)

    to_remove = ids[:5]
    rest = ids[5:]

    assert list(crud.image.get_id_list(db)) == ids
    response_1 = client.delete("/images/multiple", json=to_remove)
    assert response_1.status_code == 401

    assert list(crud.image.get_id_list(db)) == ids
    response_2 = client.delete(
        "/images/multiple", json=to_remove, headers=superuser_token_headers
    )
    assert response_2.status_code == 204
    assert response_2.content == b""

    assert list(crud.image.get_id_list(db)) == rest
    response_3 = client.delete(
        "/images/multiple", json=[456465465], headers=superuser_token_headers
    )
    assert response_3.status_code == 404


@mock.patch("app.crud.crud_image.process_image_content")
def test_remove_image(pic_m, client: TestClient, db: Session, superuser_token_headers):
    pic_m.side_effect = simulation_image_process

    image_db = crud.image.create(db, obj_in=ImageCreate(content=b"content"))
    response_1 = client.delete("/images/%d" % image_db.id)
    assert response_1.status_code == 401

    response_2 = client.delete(
        "/images/%d" % image_db.id, headers=superuser_token_headers
    )
    assert response_2.status_code == 204
    assert response_2.content == b""

    response_3 = client.delete("/images/456465465", headers=superuser_token_headers)
    assert response_3.status_code == 404
