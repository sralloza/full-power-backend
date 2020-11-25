"""Routes for manage bot conversations."""

from datetime import datetime
from json import dumps

from fastapi import APIRouter, Depends, Query, Response

from app import crud
from app.api.dependencies.database import get_db
from app.api.dependencies.security import get_current_user
from app.core.bot import detect_end, detect_intent_texts
from app.core.health_data import detect_main_problem, process_health_data
from app.models import HealthData, User
from app.schemas.bot import Msg
from app.schemas.conversation import ConversationCreate
from app.schemas.health_data import HealthDataCreate, HealthDataUpdate
from logging import getLogger

router = APIRouter()
logger = getLogger(__name__)


@router.post("/process-msg", response_model=ConversationCreate)
def bot_message_post(
    *,
    db=Depends(get_db),
    input_pack: Msg,
    user: User = Depends(get_current_user),
    lang: str = Query("en"),
    response: Response,
):
    """Sends a message to the bot and returns the response back."""

    health_data = None
    message = input_pack.msg
    logger.debug("User's message: %r", message)

    df_response = detect_intent_texts(user.id, message, lang)
    fulfillment_text = df_response["fulfillmentText"]

    parameters = df_response["parameters"]
    intent = df_response["intent"]["displayName"]

    is_end = detect_end(df_response)

    current_health_data = (
        db.query(HealthData).filter_by(valid=False, user_id=user.id).first()
    )
    if parameters:
        parameters["user_id"] = user.id

        if current_health_data:
            if is_end:
                parameters["timestamp"] = datetime.now()

            logger.debug("parameters=%r", parameters)
            health_data = HealthDataUpdate(**parameters, valid=is_end)
            crud.health_data.update(db, db_obj=current_health_data, obj_in=health_data)
        else:
            logger.debug("parameters=%r", parameters)
            health_data = HealthDataCreate(**parameters, valid=is_end)
            crud.health_data.create(db, obj_in=health_data)

    if is_end:
        hole_data = db.query(HealthData).filter_by(id=current_health_data.id).first()
        health_data_result = process_health_data(hole_data)
        main_problem_text = detect_main_problem(health_data_result, lang=lang)
        fulfillment_text = f"{fulfillment_text}. {main_problem_text}"
        response.headers["health-data-result"] = dumps(health_data_result)

    conversation = ConversationCreate(
        user_msg=message, bot_msg=fulfillment_text, intent=intent, user_id=user.id
    )
    crud.conversation.create(db, obj_in=conversation)

    return conversation
