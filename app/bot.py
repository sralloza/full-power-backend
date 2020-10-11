import os
from typing import Optional

import dialogflow
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from .users import User, get_current_user

router = APIRouter()


def detect_intent_texts(project_id, session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input
        )
        return response


class UserInput(BaseModel):
    user_input: str = Field(..., example="Hi bot! What time is it?")


class BotMessage(BaseModel):
    user_input: str = Field(..., example="Hi bot! What time is it?")
    bot_output: str = Field(..., example="Hi! It's 20:30.")
    intent: Optional[str]


@router.post("/bot-message", response_model=BotMessage)
async def bot_messsage_endpoint(
    input_pack: UserInput, user: User = Depends(get_current_user)
):
    user_id = user.id
    message = input_pack.user_input
    project_id = os.getenv("DIALOGFLOW_PROJECT_ID")

    response = detect_intent_texts(project_id, user_id, message, "en")
    fulfillment_text = response.query_result.fulfillment_text
    intent = response.query_result.intent.display_name
    os.environ["intent"] = intent

    return BotMessage(user_input=message, bot_output=fulfillment_text, intent=intent)


@router.get("/messages")
def bot_messages():
    response_text = None
    if os.getenv("intent") == "Bot language":
        response_text = {"message": "hola"}
    return response_text
