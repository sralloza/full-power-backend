from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.schemas.conversation import ConversationCreate, ConversationUpdate
from app.tests.utils.utils import random_int, random_lower_string


def test_create_conversation(db: Session):
    user_id = random_int()
    intent = random_lower_string()
    bot_msg = random_lower_string()
    user_msg = random_lower_string()
    conversation_in = ConversationCreate(
        bot_msg=bot_msg, user_msg=user_msg, user_id=user_id, intent=intent
    )
    conversation = crud.conversation.create(db, obj_in=conversation_in)

    assert conversation.user_id == user_id
    assert conversation.bot_msg == bot_msg
    assert conversation.user_msg == user_msg
    assert conversation.intent == intent
    assert hasattr(conversation, "id")
    assert conversation.id


def test_get_conversation(db: Session):
    user_id = random_int()
    intent = random_lower_string()
    bot_msg = random_lower_string()
    user_msg = random_lower_string()
    conversation_in = ConversationCreate(
        bot_msg=bot_msg, user_msg=user_msg, user_id=user_id, intent=intent
    )
    conversation = crud.conversation.create(db, obj_in=conversation_in)
    conversation_2 = crud.conversation.get(db, id=conversation.id)

    assert conversation_2
    assert conversation_2.user_id == conversation.user_id
    assert conversation_2.bot_msg == conversation.bot_msg
    assert conversation_2.user_msg == conversation.user_msg
    assert conversation_2.intent == conversation.intent
    assert conversation_2.id == conversation.id
    assert jsonable_encoder(conversation) == jsonable_encoder(conversation_2)


def test_update_conversation(db: Session):
    user_id = random_int()
    intent = random_lower_string()
    bot_msg = random_lower_string()
    user_msg = random_lower_string()
    conversation_in = ConversationCreate(
        bot_msg=bot_msg, user_msg=user_msg, user_id=user_id, intent=intent
    )
    conversation = crud.conversation.create(db, obj_in=conversation_in)

    new_bot_msg = random_lower_string()
    new_user_msg = random_lower_string()
    conversation_in_update = ConversationUpdate(
        bot_msg=new_bot_msg, user_msg=new_user_msg
    )
    crud.conversation.update(db, db_obj=conversation, obj_in=conversation_in_update)
    conversation_2 = crud.conversation.get(db, id=conversation.id)

    assert conversation_2
    assert conversation_2.intent == intent
    assert conversation_2.bot_msg == new_bot_msg
    assert conversation_2.user_msg == new_user_msg


def test_get_conversations_from_user(db: Session):
    user_id = random_int()
    convs = []
    for _ in range(7):
        intent = random_lower_string()
        bot_msg = random_lower_string()
        user_msg = random_lower_string()
        conversation_in = ConversationCreate(
            bot_msg=bot_msg, user_msg=user_msg, user_id=user_id, intent=intent
        )
        convs.append(crud.conversation.create(db, obj_in=conversation_in))

    real_convs = crud.conversation.get_user(db, user_id=user_id)
    assert real_convs == convs
