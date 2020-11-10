"""Bot related code."""

import json
from pathlib import Path

import dialogflow
from google.oauth2 import service_account

from app.core.config import settings
from app.schemas.conversation import ConversationCreate
from app.schemas.health_data import HealthDataCreate

algorithm = {
    "get_up": (
        "Congratulations, continue because the regularity of the time to get up is essential for a quality sleep.",
        "The regularity of the time to get up is essential for quality sleep. See the sleep chapter.",
    ),
    "sleep": (
        "Well done! Persevere in keeping enough sleep each night, otherwise the old problems may return ;-)",
        "If you don't get enough sleep, you risk increasing your sleep deficit. See the sleep chapter.",
    ),
    "screen": (
        "Compliment We realize that this is difficult. By avoiding screens you double the amount of deep sleep, the most restful every night ...",
        "Yep, it's not easy. We understand well. However, by avoiding screens you double the amount of deep sleep, the most recovering each night... See the sleep chapter.",
    ),
    "bedroom": (
        "It happened! Well done. These small changes greatly promote quality sleep.",
        "A cool, dark and quiet bedroom can greatly improve the quality of sleep. Wouldn't it be worth it? See the sleep chapter.",
    ),
    "stress": (
        "Super good news! Stress is the number one enemy of restful sleep. Continue to anchor this habit by being rigorous in this practice for another 1 or 2 months. It will become as automatic as brushing your teeth!",
        "Stress is the number one enemy of restful sleep. Explore the different ways to reduce your stress, if meditation is not your cup of tea, for example try a good bath, reading, music or a good walk in the evening. More ideas in the sleep chapter.",
    ),
}


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
