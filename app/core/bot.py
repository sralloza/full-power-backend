"""Bot related code."""

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


def detect_intent_texts(session_id: int, text: str, language_code: str) -> dict:
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(settings.dialogflow_project_id, session_id)

    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)
    return MessageToDict(response.query_result)
