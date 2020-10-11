import os
from typing import List

from app.bot.crud import create_conversation, list_all_conversations, list_conversations
from app.database.models import User
from app.security import get_current_user
from fastapi import APIRouter, Depends

from .schemas import ConversationCreate, UserInput
from .utils import detect_intent_texts

router = APIRouter()


@router.post("/bot-message", response_model=ConversationCreate)
async def bot_messsage_endpoint(
    input_pack: UserInput, user: User = Depends(get_current_user)
):
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
def bot_messages():
    response_text = None
    if os.getenv("intent") == "Bot language":
        response_text = {"message": "hola"}
    return response_text


@router.post("/conversations/user/{user_id}", response_model=schemas.Conversation)
def url_create_conversation(user_id: int, conversation: schemas.ConversationCreate):
    return create_conversation(conversation=conversation, user_id=user_id)


@router.get("/conversations/user/{user_id}", response_model=List[schemas.Conversation])
def url_list_conversation(user_id: int, skip: int = 0, limit: int = 100):
    return list_conversations(user_id=user_id, skip=skip, limit=limit)


@router.get("/conversations", response_model=List[schemas.Conversation])
def url_list_all_conversations(skip: int = 0, limit: int = 100):
    return list_all_conversations(skip=skip, limit=limit)
