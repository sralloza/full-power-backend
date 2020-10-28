"""Routes for manage bot conversations."""

import os

from fastapi import APIRouter, Depends

from app import crud
from app.api.dependencies.database import get_db
from app.api.dependencies.security import get_current_user
from app.core.bot import detect_intent_texts
from app.core.config import settings
from app.models import User
from app.schemas.bot import Msg
from app.schemas.conversation import ConversationCreate

router = APIRouter()


@router.post("/bot-message", response_model=ConversationCreate)
def bot_message_post(
    *, db=Depends(get_db), input_pack: Msg, user: User = Depends(get_current_user)
):
    """Sends a message to the bot and returns the response back."""

    user_id = user.id
    message = input_pack.msg
    project_id = settings.dialogflow_project_id

    response = detect_intent_texts(project_id, user_id, message, "en")
    fulfillment_text = response.query_result.fulfillment_text

    intent = response.query_result.intent.display_name
    os.environ["intent"] = intent

    conversation = ConversationCreate(
        user_msg=message, bot_msg=fulfillment_text, intent=intent, user_id=user.id
    )
    crud.conversation.create(db, obj_in=conversation)

    return conversation
