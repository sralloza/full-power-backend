"""Bot related code."""

import json
from pathlib import Path

import dialogflow
from google.oauth2 import service_account

from app.core.config import settings


def detect_end(response):
    is_end = False
    try:
        if response.query_result.diagnostic_info:
            is_end = True
    except AttributeError:
        pass
    return is_end


def parse_parameters_field(fields):
    real = {}
    fields = dict(fields)
    for k, v in fields.items():
        real[k] = str(v).strip()
        for attr in dir(v):
            if not attr.endswith("value"):
                continue
            value = getattr(v, attr)
            if not value:
                continue
            real[k] = value
            break
    return real


def get_credentials():
    json_string = Path(settings.google_application_credentials).read_text()
    info = json.loads(json_string)
    credentials = service_account.Credentials.from_service_account_info(info)
    return credentials


def detect_intent_texts(session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(settings.dialogflow_project_id, session_id)

    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)
    return response
