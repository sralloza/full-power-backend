"""Routes for manage bot conversations."""

import os

from fastapi import APIRouter, Depends

from app.conversations.crud import create_conversation
from app.conversations.schemas import ConversationCreate
from app.database.models import User
from app.security.utils import get_current_user

from .schemas import UserInput
from .utils import detect_intent_texts

router = APIRouter()


@router.post("/bot-message", response_model=ConversationCreate)
def bot_message_post(input_pack: UserInput, user: User = Depends(get_current_user)):
    """Sends a message to the bot and returns the response back."""

    user_id = user.id
    message = input_pack.user_msg
    project_id = os.getenv("DIALOGFLOW_PROJECT_ID")

    response = detect_intent_texts(project_id, user_id, message, "en")
    fulfillment_text = response.query_result.fulfillment_text

    intent = response.query_result.intent.display_name
    os.environ["intent"] = intent

    conversation = ConversationCreate(
        user_msg=message, bot_msg=fulfillment_text, intent=intent
    )
    create_conversation(conversation, user_id)

    return conversation


@router.get("/messages")
def messages_get():
    response_text = None
    if os.getenv("intent") == "Bot language":
        response_text = {"message": "hola"}
    return response_text
