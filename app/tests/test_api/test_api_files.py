from fastapi.testclient import TestClient
from sqlalchemy.orm.session import Session

from app import crud
from app.core.files import get_file_id_from_name
from app.schemas.file import FileCreate, FileCreateInner, FileUpdate


def fci(content: str, name: str, title: str, lang: str = "es"):
    file_id = get_file_id_from_name(name, lang)
    return FileCreateInner(
        content=content, id=file_id, name=name, title=title, lang=lang
    )


def test_list_files(db: Session, client: TestClient):
    crud.file.create(db, obj_in=fci("data", "vitamins.p", "n", "ru"))
    crud.file.create(db, obj_in=fci("data", "vitamins.a", "b", "ru"))
    response_1 = client.get("/files?lang=es")
    assert response_1.status_code == 200
    assert response_1.json() == []

    response_2 = client.get("/files?lang=ru")
    assert response_2.status_code == 200
    assert response_2.json() == [
        {"name": "vitamins.a", "title": "b", "lang": "ru"},
        {"name": "vitamins.p", "title": "n", "lang": "ru"},
    ]


def test_list_files_grouped(db: Session, client: TestClient):
    crud.file.create(db, obj_in=fci("data", "vitamins.t1", "t", "ru"))
    crud.file.create(db, obj_in=fci("data", "vitamins.t2", "t", "ru"))
    crud.file.create(db, obj_in=fci("data", "vitamins.t2", "t", "es"))

    response = client.get("/files/all")
    assert response.status_code == 200

    data = response.json()
    assert data == [
        {"name": "vitamins.t1", "langs": ["ru"]},
        {"name": "vitamins.t2", "langs": ["es", "ru"]},
    ]


def test_get_files_by_name(db: Session, client: TestClient):
    crud.file.create(db, obj_in=fci("vits", "vitamins.v1", "i", "en"))
    crud.file.create(db, obj_in=fci("vits", "vitamins.v2", "i", "en"))
    crud.file.create(db, obj_in=fci("vits", "vitamins.v3", "i", "en"))

    names = ["vitamins.v1", "vitamins.v2", "vitamins.v3"]
    response_ok = client.get("/files/multi", json=names)
    assert response_ok.status_code == 200
    files = response_ok.json()
    assert files == [
        {"name": "vitamins.v1", "content": "vits", "title": "i", "lang": "en"},
        {"name": "vitamins.v2", "content": "vits", "title": "i", "lang": "en"},
        {"name": "vitamins.v3", "content": "vits", "title": "i", "lang": "en"},
    ]

    other_names = names + ["invalid"]
    response_fail = client.get("/files/multi", json=other_names)
    assert response_fail.status_code == 404
    detail = response_fail.json()["detail"]
    assert detail == "File with name=invalid and lang=en does not exist"


def test_get_file_by_name(db: Session, client: TestClient):
    response_1 = client.get("/files/vitamins.sdaflk")
    assert response_1.status_code == 404
    detail = response_1.json()["detail"]
    assert detail == "File with name=vitamins.sdaflk and lang=en does not exist"

    crud.file.create(db, obj_in=fci("vits-ensured", "vitamins.ensured", "i", "en"))
    response_2 = client.get("/files/vitamins.ensured")
    assert response_2.status_code == 200
    assert response_2.json()["name"] == "vitamins.ensured"
    assert response_2.json()["lang"] == "en"
    assert response_2.json()["title"] == "i"
    assert response_2.json()["content"] == "vits-ensured"


def test_create_file(db: Session, client: TestClient, superuser_token_headers):
    file_in = FileCreate(
        content="vits power", name="vitamins.power", title="c", lang="fr"
    )
    response_1 = client.post("/files", data=file_in.json())
    assert response_1.status_code == 401

    response_2 = client.post(
        "/files?lang=ch", data=file_in.json(), headers=superuser_token_headers
    )
    assert response_2.status_code == 201
    assert response_2.json()["name"] == "vitamins.power"
    assert response_2.json()["lang"] == "ch"
    assert response_2.json()["title"] == "c"
    assert "content" not in response_2.json()

    file_db = crud.file.get_by_name(db, name="vitamins.power", lang="ch")
    assert file_db.name == "vitamins.power"
    assert file_db.lang == "ch"
    assert file_db.content == "vits power"
    assert file_db.title == "c"

    response_3 = client.post(
        "/files?lang=ch", data=file_in.json(), headers=superuser_token_headers
    )
    assert response_3.status_code == 409
    error = f"File with name=vitamins.power and lang=ch already exists"
    assert response_3.json()["detail"] == error


def test_create_multiple_files(client: TestClient, superuser_token_headers):
    files_create = [
        fci("vits", "vitamins.v1", "i", "en").dict(),
        fci("vits", "vitamins.v2", "i", "en").dict(),
        fci("vits", "vitamins.v3", "i", "en").dict(),
    ]

    response_ok = client.post(
        "/files/multi", json=files_create, headers=superuser_token_headers
    )
    assert response_ok.status_code == 201
    files = response_ok.json()
    assert files == [
        {"name": "vitamins.v1", "title": "i", "lang": "en"},
        {"name": "vitamins.v2", "title": "i", "lang": "en"},
        {"name": "vitamins.v3", "title": "i", "lang": "en"},
    ]


def test_update_file(db: Session, client: TestClient, superuser_token_headers):
    crud.file.create(db, obj_in=fci("old", "vitamins.ut", "b", "it"))
    file_in = FileUpdate(content="new", title="k", lang="pt", name="vitamins.new")

    response_1 = client.put("/files/vitamins.ut?lang=it", data=file_in.json())
    assert response_1.status_code == 401

    response_2 = client.put(
        "/files/vitamins.ut?lang=it",
        data=file_in.json(),
        headers=superuser_token_headers,
    )
    assert response_2.status_code == 200

    assert response_2.json()["name"] == "vitamins.new"
    assert response_2.json()["title"] == "k"
    assert response_2.json()["lang"] == "pt"
    assert "content" not in response_2.json()

    # db.commit()  # For some reason fails without this
    assert crud.file.get_by_name(db, name="vitamins.ut", lang="it") is None
    new_file_db = crud.file.get_by_name(db, name="vitamins.new", lang="pt")
    assert new_file_db.name == "vitamins.new"
    assert new_file_db.title == "k"
    assert new_file_db.lang == "pt"
    assert new_file_db.content == "new"


def test_remove_multiple_files(
    db: Session, client: TestClient, superuser_token_headers
):
    response_1 = client.delete(
        "/files/multiple", json=[{"name": "vitamins.sdfsdf", "lang": "ch"}]
    )
    assert response_1.status_code == 401

    crud.file.create(db, obj_in=fci("c", "vitamins.53", "53", "ru"))
    crud.file.create(db, obj_in=fci("c", "vitamins.54", "54", "ru"))
    crud.file.create(db, obj_in=fci("c", "vitamins.55", "55", "ru"))
    crud.file.create(db, obj_in=fci("c", "vitamins.56", "56", "ru"))
    crud.file.create(db, obj_in=fci("c", "vitamins.57", "57", "ru"))

    remaining = {x.name for x in crud.file.get_db_file_list(db, lang="ru")}
    assert remaining == {
        "vitamins.53",
        "vitamins.54",
        "vitamins.55",
        "vitamins.56",
        "vitamins.57",
    }

    response_2 = client.delete(
        "/files/multiple",
        json=[
            {"name": "vitamins.53", "lang": "ru"},
            {"name": "vitamins.54", "lang": "ru"},
            {"name": "vitamins.55", "lang": "ru"},
        ],
        headers=superuser_token_headers,
    )
    assert response_2.status_code == 204
    assert response_2.content == b""

    remaining = {x.name for x in crud.file.get_db_file_list(db, lang="ru")}
    assert remaining == {"vitamins.56", "vitamins.57"}

    response_3 = client.delete(
        "/files/multiple",
        json=[
            {"name": "vitamins.57", "lang": "ru"},
            {"name": "vitamins.58", "lang": "ru"},
        ],
        headers=superuser_token_headers,
    )
    assert response_3.status_code == 404
    detail = "File with name=vitamins.58 and lang=ru does not exist"
    assert response_3.json()["detail"] == detail

    remaining = {x.name for x in crud.file.get_db_file_list(db, lang="ru")}
    assert remaining == {"vitamins.56"}


def test_remove_file(db: Session, client: TestClient, superuser_token_headers):
    response_1 = client.delete("/files/vitamins.done")
    assert response_1.status_code == 401

    crud.file.create(db, obj_in=fci("a", "vitamins.done", "s", "es"))

    response_2 = client.delete(
        "/files/vitamins.done?lang=gr", headers=superuser_token_headers
    )
    assert response_2.status_code == 404
    detail = response_2.json()["detail"]
    assert detail == "File with name=vitamins.done and lang=gr does not exist"

    crud.file.create(db, obj_in=fci("a", "vitamins.done", "z", "gr"))

    response_3 = client.delete(
        "/files/vitamins.done?lang=gr", headers=superuser_token_headers
    )
    assert response_3.status_code == 204
    assert response_3.content == b""
