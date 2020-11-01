from unittest import mock

from app import crud
from app.schemas.conversation import Conversation, ConversationCreate


@mock.patch("app.api.routes.bot.detect_intent_texts")
def test_process_msg(dit_m, client, db, normal_user_token_headers):
    dit_m.return_value.query_result.fulfillment_text = "this is the bot message"
    dit_m.return_value.query_result.intent.display_name = "this is the intent"
    response = client.post(
        "/bot/process-msg",
        json={"msg": "this is the user message"},
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    conv = ConversationCreate(**response.json())

    assert conv.user_msg == "this is the user message"
    assert conv.bot_msg == "this is the bot message"
    assert conv.intent == "this is the intent"
    dit_m.assert_called_once_with(mock.ANY, mock.ANY, conv.user_msg, "en")

    convs_db = crud.conversation.get_multi(db)
    assert len(convs_db) == 1
    conv_db = convs_db[0]

    assert conv == ConversationCreate.parse_obj(Conversation.from_orm(conv_db))
