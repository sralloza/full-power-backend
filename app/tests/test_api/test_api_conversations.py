from typing import List

from pydantic import parse_obj_as
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app import crud
from app.schemas.conversation import Conversation, ConversationCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_int, random_lower_string


def test_conversation_post(client: TestClient, db: Session, superuser_token_headers):
    conversation_in = ConversationCreate(
        user_id=random_int(),
        bot_msg=random_lower_string(),
        user_msg=random_lower_string(),
        intent=random_lower_string(),
    )
    response = client.post(
        "/conversations", json=conversation_in.dict(), headers=superuser_token_headers
    )
    assert response.status_code == 201

    conversation_created = Conversation.parse_obj(response.json())
    assert conversation_created.id

    conversation_db = crud.conversation.get(db, id=conversation_created.id)
    assert conversation_created == Conversation.from_orm(conversation_db)


def test_conversation_get_or_404(
    client: TestClient, db: Session, superuser_token_headers
):
    response = client.get("/conversations/56456", headers=superuser_token_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Conversation with id=56456 does not exist"

    conversation_in = ConversationCreate(
        user_id=random_int(),
        bot_msg=random_lower_string(),
        user_msg=random_lower_string(),
        intent=random_lower_string(),
    )
    conv_db = crud.conversation.create(db, obj_in=conversation_in)
    response = client.get(
        "/conversations/%d" % conv_db.id, headers=superuser_token_headers
    )
    assert response.status_code == 200

    conv = Conversation.parse_obj(response.json())
    assert conv.id
    assert conv == Conversation.from_orm(conv_db)


def test_conversation_get_from_user(
    client: TestClient, db: Session, superuser_token_headers: dict
):
    user_id = random_int()
    response_1 = client.get(
        f"/conversations/user/{user_id}", headers=superuser_token_headers
    )
    assert response_1.status_code == 404
    assert response_1.json()["detail"] == f"User with id={user_id} does not exist"

    user = create_random_user(db)
    user_id = user.id

    def get_conv():
        return ConversationCreate(
            user_id=user_id,
            bot_msg=random_lower_string(),
            user_msg=random_lower_string(),
            intent=random_lower_string(),
        )

    convs = [get_conv() for _ in range(7)]
    saved = []

    for conv in convs:
        conv_db = crud.conversation.create(db, obj_in=conv)
        saved.append(Conversation.from_orm(conv_db))

    response_2 = client.get(
        f"/conversations/user/{user_id}", headers=superuser_token_headers
    )
    assert response_2.status_code == 200
    real_convs = parse_obj_as(List[Conversation], response_2.json())
    assert real_convs == saved


def test_conversation_get_from_all_users(
    client: TestClient, db: Session, superuser_token_headers: dict
):
    convs_db = crud.conversation.get_multi(db)
    convs = [Conversation.from_orm(x) for x in convs_db]

    response = client.get("/conversations", headers=superuser_token_headers)
    assert response.status_code == 200
    real_convs = parse_obj_as(List[Conversation], response.json())
    assert real_convs == convs


def test_conversation_delete(client: TestClient, db: Session, superuser_token_headers):
    conversation_in = ConversationCreate(
        user_id=random_int(),
        bot_msg=random_lower_string(),
        user_msg=random_lower_string(),
        intent=random_lower_string(),
    )
    conv_db = crud.conversation.create(db, obj_in=conversation_in)

    response = client.delete(
        f"/conversations/{conv_db.id}", headers=superuser_token_headers
    )
    assert response.status_code == 204
    assert response.content == b""


def test_remove_nonexisting_conv(client: TestClient, superuser_token_headers):
    response = client.delete("/conversations/198526", headers=superuser_token_headers)

    error = response.json()
    assert response.status_code == 404
    assert error["detail"] == "Conversation with id=198526 does not exist"
