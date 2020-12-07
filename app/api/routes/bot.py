"""Routes for manage bot conversations."""

from datetime import datetime
from json import dumps
from logging import getLogger

from fastapi import APIRouter, Depends, HTTPException, Query, Response

from app import crud
from app.api.dependencies.database import get_db
from app.api.dependencies.security import get_current_user
from app.core.bot import get_df_response
from app.core.health_data import detect_main_problem, process_health_data
from app.models import User
from app.schemas.bot import Msg
from app.schemas.conversation import ConversationCreate
from app.schemas.health_data import HealthDataCreate, HealthDataUpdate

router = APIRouter()
logger = getLogger(__name__)


@router.post(
    "/process-msg",
    response_model=ConversationCreate,
    responses={500: {"description": "HealthData was not saved before processing"}},
    summary="Process user message",
)
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

    df_resp = get_df_response(user.id, message, lang)
    logger.debug("Bot response: %r", df_resp)
    pending_hd = crud.health_data.get_pending_from_user(db, user_id=user.id)

    if df_resp.parameters:
        df_resp.parameters.update(dict(user_id=user.id, timestamp=datetime.now()))

        if pending_hd:
            health_data = HealthDataUpdate(**df_resp.parameters, valid=df_resp.is_end)
            crud.health_data.update(db, db_obj=pending_hd, obj_in=health_data)
        else:
            health_data = HealthDataCreate(**df_resp.parameters, valid=df_resp.is_end)
            crud.health_data.create(db, obj_in=health_data)

    if df_resp.is_end:
        try:
            filled_hd = crud.health_data.get(db, id=pending_hd.id)
            assert filled_hd is not None
        except (AssertionError, AttributeError) as exc:
            raise HTTPException(
                500, "HealthData was not saved before processing"
            ) from exc

        result = process_health_data(filled_hd)
        problem_explanation = detect_main_problem(result, lang=lang)
        df_resp.bot_msg = f"{df_resp.bot_msg}. {problem_explanation}"
        response.headers["health-data-result"] = dumps(result)

    conversation = ConversationCreate(
        user_msg=message, user_id=user.id, **df_resp.dict()
    )
    crud.conversation.create(db, obj_in=conversation)

    return conversation
