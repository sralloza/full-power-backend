"""Routes for manage bot conversations."""

import re
from datetime import datetime
from logging import getLogger

from fastapi import APIRouter, Body, Depends, HTTPException, Query, Response

from app import crud
from app.api.dependencies.database import get_db
from app.api.dependencies.security import get_current_user
from app.core.bot import get_df_response, response_to_question
from app.core.config import settings
from app.core.health_data import hdprocessor
from app.models import User
from app.schemas.bot import QuestionResponse
from app.schemas.conversation import ConversationCreate, ConversationOut
from app.schemas.health_data import HealthDataCreate, HealthDataUpdate

router = APIRouter(
    dependencies=[Depends(get_current_user)], prefix="/bot", tags=["bot"]
)
logger = getLogger(__name__)


@router.post(
    "/process-msg",
    response_model=ConversationOut,
    responses={
        500: {"description": "HealthData was not saved before processing"},
        400: {"description": "'msg' and 'question_response' are mutually exlusive"},
    },
    summary="Process user message",
)
def bot_message_post(
    *,
    db=Depends(get_db),
    user: User = Depends(get_current_user),
    lang: str = Query("en"),
    response: Response,
    msg: str = Body(None),
    question_response: QuestionResponse = Body(None),
):
    """Sends a message to the bot and returns the response back. You need to pass
    'msg' or 'question_response', but no both.

    The final intent includes two headers:

    - **X-Problems-Parsed** - list of parsed problems
    - **X-Health-Data-Result** - result of the health data algorithm
    """

    if msg and question_response:
        raise HTTPException(400, "'msg' and 'question_response' are mutually exlusive")

    health_data = None
    message = msg
    logger.debug("User's message: %r", message)

    if question_response:
        return ConversationOut(
            display_type="default",
            bot_msg=response_to_question(question_response, lang),
            intent="notification-question-response",
            user_msg=question_response.user_response,
            user_id=user.id,
        )

    notification_question_match = re.search(settings.bot_question_message_flag, message)

    if notification_question_match:
        logger.debug("Notification question detected, returning echo")
        message = re.sub(settings.bot_question_message_flag, "", message)
        return ConversationOut(
            display_type="yes_no",
            bot_msg=message,
            intent="notification-question-echo",
            user_msg=message,
            user_id=user.id,
        )

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

        result = hdprocessor.process_health_data(filled_hd)
        problems = hdprocessor.classify_problems(result)
        problem_explanation = hdprocessor.gen_report(problems, lang=lang)
        df_resp.bot_msg = f"{df_resp.bot_msg}\n{problem_explanation}"
        response.headers["X-Problems-Parsed"] = problems.json()
        response.headers["X-Health-Data-Result"] = result.json()

    conversation = ConversationCreate(
        user_msg=message, user_id=user.id, **df_resp.dict()
    )
    return crud.conversation.create(db, obj_in=conversation)
