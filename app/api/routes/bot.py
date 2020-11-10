"""Routes for manage bot conversations."""

from fastapi import APIRouter, Depends, Query

from app import crud
from app.api.dependencies.database import get_db
from app.api.dependencies.security import get_current_user
from app.core.bot import detect_intent_texts, fix_conversation, parse_parameters_field
from app.core.config import settings
from app.models import HealthData, User
from app.schemas.bot import Msg
from app.schemas.conversation import ConversationCreate
from app.schemas.health_data import HealthDataCreate, HealthDataUpdate

router = APIRouter()

@router.post("/process-msg", response_model=ConversationCreate)
def bot_message_post(
    *,
    db=Depends(get_db),
    input_pack: Msg,
    user: User = Depends(get_current_user),
    lang: str = Query("en"),
):
    """Sends a message to the bot and returns the response back."""

    health_data = None
    message = input_pack.msg

    response = detect_intent_texts(
        settings.dialogflow_project_id, user.id, message, lang
    )
    fulfillment_text = response.query_result.fulfillment_text

    intent = response.query_result.intent.display_name

    is_end = False
    try:
        if response.query_result.diagnostic_info:
            is_end = True
    except AttributeError:
        pass

    if response.query_result.parameters.fields:
        real = parse_parameters_field(response.query_result.parameters.fields)

        current_health_data = (
            db.query(HealthData).filter_by(valid=False, user_id=user.id).first()
        )
        real["user_id"] = user.id
        if current_health_data:
            health_data = HealthDataUpdate(**real, valid=is_end)
            crud.health_data.update(db, db_obj=current_health_data, obj_in=health_data)
        else:
            health_data = HealthDataCreate(**real, valid=is_end)
            crud.health_data.create(db, obj_in=health_data)

    conversation = ConversationCreate(
        user_msg=message, bot_msg=fulfillment_text, intent=intent, user_id=user.id
    )
    crud.conversation.create(db, obj_in=conversation)

    if health_data is not None:
        fix_conversation(conversation, health_data)

    return conversation
