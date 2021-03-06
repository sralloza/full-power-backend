"""Bot related code."""

import logging

import dialogflow
from fastapi import HTTPException
from google.api_core.exceptions import PermissionDenied
from google.protobuf.json_format import MessageToDict

from app.core.config import settings
from app.schemas.bot import DFResponse, QuestionResponse
from app.utils.translate import i18n

logger = logging.getLogger(__name__)


def detect_end(df_response: dict):
    is_end = False
    try:
        if df_response["diagnosticInfo"]:
            is_end = True
    except KeyError:
        pass
    return is_end


def get_df_response(session_id: int, text: str, language_code: str) -> DFResponse:
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(settings.dialogflow_project_id, session_id)

    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    try:
        response = session_client.detect_intent(
            session=session, query_input=query_input
        )
    except PermissionDenied:
        logger.exception("Dialogflow permission denied")
        raise HTTPException(500, "Dialogflow permission denied")

    response = MessageToDict(response.query_result)
    return parse_df_response(response)


def parse_df_response(df_response: dict):
    return DFResponse(
        bot_msg=df_response["fulfillmentText"],
        intent=df_response["intent"]["displayName"],
        is_end=detect_end(df_response),
        parameters=df_response.get("parameters", dict()),
    )


def response_to_question(question_response: QuestionResponse, lang: str) -> str:
    i18n.set("locale", lang)
    problem, pos = question_response.question_id.split(".")
    user_response = str(question_response.user_response).lower()
    key = f"response.{problem}.{user_response}.resp{pos}"
    return i18n.t(key)
