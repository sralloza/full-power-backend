"""Bot related code."""

from app.schemas.bot import DFResponse
import json
from pathlib import Path

import dialogflow
from google.oauth2 import service_account
from google.protobuf.json_format import MessageToDict

from app.core.config import settings


def detect_end(df_response: dict):
    is_end = False
    try:
        if df_response["diagnosticInfo"]:
            is_end = True
    except KeyError:
        pass
    return is_end


def get_credentials():
    json_string = Path(settings.google_application_credentials).read_text()
    info = json.loads(json_string)
    credentials = service_account.Credentials.from_service_account_info(info)
    return credentials


def get_df_response(session_id: int, text: str, language_code: str) -> DFResponse:
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(settings.dialogflow_project_id, session_id)

    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)
    response = MessageToDict(response.query_result)
    return parse_df_response(response)


def parse_df_response(df_response: dict):
    return DFResponse(
        bot_msg=df_response["fulfillmentText"],
        intent=df_response["intent"]["displayName"],
        is_end=detect_end(df_response),
        parameters=df_response.get("parameters", dict()),
    )
