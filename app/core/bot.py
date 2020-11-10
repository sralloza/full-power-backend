"""Bot related code."""

import json
from pathlib import Path

import dialogflow
from fastapi.exceptions import HTTPException
from google.oauth2 import service_account

from app.core.config import settings
from app.schemas.conversation import ConversationCreate
from app.schemas.health_data import HealthDataCreate

algorithm = {
    "get_up": {
        "en": (
            "Congratulations, continue because the regularity of the time to get up is essential for a quality sleep.",
            "The regularity of the time to get up is essential for quality sleep. See the sleep chapter.",
        ),
        "es": (
            "Enhorabuena, continúe porque la regularidad del tiempo para levantarse es fundamental para un sueño de calidad.",
            "La regularidad del tiempo para levantarse es fundamental para un sueño de calidad. Consulte el capítulo sobre el sueño.",
        ),
        "fr": (
            "Félicitations, continuez car la régularité de l’heure du levé est indispensable pour un sommeil de qualité.",
            "La régularité de l’heure du levé est indispensable pour un sommeil de qualité. Consultez le chapitre sommeil.",
        ),
    },
    "sleep": {
        "en": (
            "Well done! Persevere in keeping enough sleep each night, otherwise the old problems may return ;-)",
            "If you don't get enough sleep, you risk increasing your sleep deficit. See the sleep chapter.",
        ),
        "es": (
            "Bien hecho ! Persevera en dormir lo suficiente cada noche, de lo contrario, los viejos problemas pueden regresar ;-)",
            "Si no duerme lo suficiente, corre el riesgo de aumentar su déficit de sueño. Consulte el capítulo sobre el sueño.",
        ),
        "fr": (
            "Bravo ! Persévérez à conserver une durée suffisante de sommeil chaque nuit, sinon les anciens problèmes peuvent revenir ;-)",
            "Si vous ne vous offrez pas un temps de sommeil suffisant, vous risquez de creuser votre déficit de sommeil. Consultez le chapitre sommeil.",
        ),
    },
    "screen": {
        "en": (
            "Compliment We realize that this is difficult. By avoiding screens you double the amount of deep sleep, the most restful every night ...",
            "Yep, it's not easy. We understand well. However, by avoiding screens you double the amount of deep sleep, the most recovering each night... See the sleep chapter.",
        ),
        "es": (
            "Elogio… Nos damos cuenta de que esto es difícil. Al evitar las pantallas, duplica la cantidad de sueño profundo, el más reparador cada noche",
            "Sí, no es fácil. Entendemos bien. Sin embargo, al evitar las pantallas, duplica la cantidad de sueño profundo, el que más se recupera cada noche ... Consulte el capítulo sobre el sueño.",
        ),
        "fr": (
            "Compliment… Nous sommes conscients que cela est difficile. En évitant les écrans vous doublez la quantité de sommeil profond, le plus récupérateur chaque nuit… 	",
            "Eh oui, ce n’est pas facile. Nous comprenons bien. Toutefois, en évitant les écrans vous doublez la quantité de sommeil profond, le plus récupérateur chaque nuit… Consultez le chapitre sommeil.",
        ),
    },
    "bedroom": {
        "en": (
            "It happened! Well done. These small changes greatly promote quality sleep.",
            "A cool, dark and quiet bedroom can greatly improve the quality of sleep. Wouldn't it be worth it? See the sleep chapter.",
        ),
        "es": (
            "¡Ocurrió! Bien hecho. Estos pequeños cambios promueven en gran medida un sueño de calidad.",
            "Un dormitorio fresco, oscuro y silencioso puede mejorar enormemente la calidad del sueño. ¿No valdría la pena ? Consulte el capítulo sobre el sueño.",
        ),
        "fr": (
            "Ça, s’est fait ! Bravo. Ces petits changements favorisent grandement le sommeil de qualité.",
            "Un chambre fraîche, sombre et silencieuse permet d’améliorer grandement la qualité du sommeil. Est-ce que cela ne vaudrait pas le coup ? Consultez le chapitre sommeil. ",
        ),
    },
    "stress": {
        "en": (
            "Super good news! Stress is the number one enemy of restful sleep. Continue to anchor this habit by being rigorous in this practice for another 1 or 2 months. It will become as automatic as brushing your teeth!",
            "Stress is the number one enemy of restful sleep. Explore the different ways to reduce your stress, if meditation is not your cup of tea, for example try a good bath, reading, music or a good walk in the evening. More ideas in the sleep chapter.",
        ),
        "es": (
            "¡Súper buenas noticias! El estrés es el enemigo número uno del sueño reparador. Continúe anclando este hábito siendo riguroso en esta práctica durante 1 o 2 meses más ¡Se volverá tan automático como cepillarse los dientes!",
            "El estrés es el enemigo número uno del sueño reparador. Explora las diferentes formas de reducir tu estrés, si la meditación no es lo tuyo, por ejemplo prueba un buen baño, lectura, música o un buen paseo por la noche. Más ideas en el capítulo del sueño.",
        ),
        "fr": (
            "Super bonne nouvelle ! Le stress est le premier ennemi d’un sommeil récupérateur. Continuez à ancrer cette habitude en étant rigoureux sur cette pratique encore 1 mois ou 2. Cela deviendra aussi automatique que de vous brosser les dents !",
            "Le stress est le premier ennemi d’un sommeil récupérateur. Explorez les différentes méthodes pour réduire votre stress, si la méditation n’est pas votre tasse de thé, essayez par exemple un bon bain, de la lecture, de la musique ou une bonne balade le soir. Plus d’idées dans le chapitre sommeil.",
        ),
    },
}


def fix_conversation(
    lang: str, conversation: ConversationCreate, health_data: HealthDataCreate
):
    for key, value in health_data.dict().items():
        if value is None:
            continue
        if key in algorithm:
            value = int(not value)
            if lang not in algorithm[key]:
                supported = list(algorithm[key].keys())
                raise HTTPException(400, f"language not supported ({supported})")
            response = algorithm[key][lang][value]
            conversation.bot_msg = response + "\n" + conversation.bot_msg
            break


def detect_end(response):
    is_end = False
    try:
        if response.query_result.diagnostic_info:
            is_end = True
    except AttributeError:
        pass
    return is_end


def gen_report(
    lang: str, conversation: ConversationCreate, health_data: HealthDataCreate
):
    string = ""
    for key, value in health_data.dict().items():
        if key in algorithm:
            value = int(not value)
            response = algorithm[key][lang][value]
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
