"""Bot related code."""

import json
from pathlib import Path

import dialogflow
from google.oauth2 import service_account

from app.core.config import settings


def fix_conversation(conversation: ConversationCreate, health_data: HealthDataCreate):
    for key, value in health_data.dict().items():
        if value is None:
            continue
        if key in algorithm:
            value = int(not value)
            response = algorithm[key][value]
            conversation.bot_msg = response + "\n" + conversation.bot_msg
            break


def gen_report(conversation: ConversationCreate, health_data: HealthDataCreate):
    string = ""
    for key, value in health_data.dict().items():
        if key in algorithm:
            value = int(not value)
            response = algorithm[key][value]
            string += f"{key}: {response}\n\n"

    conversation.bot_msg = string
    return conversation


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


def detect_intent_texts(project_id, session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)
    return response
