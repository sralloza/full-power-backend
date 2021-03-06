from unittest import mock

import dialogflow
import pytest
from fastapi import HTTPException
from google.api_core.exceptions import PermissionDenied

from app.core.bot import (
    detect_end,
    get_df_response,
    parse_df_response,
    response_to_question,
)
from app.schemas.bot import DFResponse, QuestionResponse


class TestGetDFResonse:
    @pytest.fixture(autouse=True)
    def mocks(self):
        self.client_m = mock.patch("dialogflow.SessionsClient").start()
        mock.patch("app.core.bot.settings.dialogflow_project_id", 600).start()
        self.mtd_m = mock.patch("app.core.bot.MessageToDict").start()
        self.parse_df_response_m = mock.patch("app.core.bot.parse_df_response").start()
        yield
        mock.patch.stopall()

    def test_ok(self):
        result = get_df_response(500, "text", "lc")
        self.client_m.assert_called_once_with()
        session_client = self.client_m.return_value
        session_client.session_path.assert_called_once_with(600, 500)
        session = session_client.session_path.return_value

        text_input = dialogflow.types.TextInput(text="text", language_code="lc")

        query_input = dialogflow.types.QueryInput(text=text_input)

        session_client.detect_intent.assert_called_once_with(
            session=session, query_input=query_input
        )
        self.mtd_m.assert_called_once_with(
            session_client.detect_intent.return_value.query_result
        )
        self.parse_df_response_m.assert_called_once_with(self.mtd_m.return_value)
        assert result == self.parse_df_response_m.return_value

    def test_fail(self):
        self.client_m.return_value.detect_intent.side_effect = PermissionDenied(
            "for some reason"
        )

        with pytest.raises(HTTPException) as exc_info:
            result = get_df_response(500, "text", "it")

        exc = exc_info.value
        assert exc.status_code == 500
        assert exc.detail == "Dialogflow permission denied"

        self.client_m.assert_called_once_with()
        session_client = self.client_m.return_value
        session_client.session_path.assert_called_once_with(600, 500)
        session_client.detect_intent.assert_called_once()

        self.mtd_m.assert_not_called()
        self.parse_df_response_m.assert_not_called()

        with pytest.raises(NameError):
            assert not result


expected = (
    dict(bot_msg="bot_msg", intent="intent", is_end=True, parameters={"value": 53}),
    dict(bot_msg="bot_msg", intent="intent", is_end=True, parameters={"var": "text"}),
    dict(bot_msg="bot_msg", intent="intent", is_end=True, parameters={}),
)
df_responses = (
    {
        "fulfillmentText": "bot_msg",
        "intent": {"name": "something", "displayName": "intent"},
        "parameters": {"value": 53},
    },
    {
        "fulfillmentText": "bot_msg",
        "intent": {"name": "something", "displayName": "intent"},
        "parameters": {"var": "text"},
    },
    {
        "fulfillmentText": "bot_msg",
        "intent": {"name": "something", "displayName": "intent"},
    },
)


@mock.patch("app.core.bot.detect_end")
@pytest.mark.parametrize("df_response,expected", zip(df_responses, expected))
def test_parse_df_response(detect_end_m, df_response, expected):
    detect_end_m.return_value = True
    expected = DFResponse(**expected)
    result = parse_df_response(df_response)
    assert result == expected


detect_end_data = (
    ({"diagnosticInfo": "something"}, True),
    ({"diagnosticInfo": 2}, True),
    ({"diagnosticInfo": True}, True),
    ({"diagnosticInfo": ""}, False),
    ({"diagnosticInfo": None}, False),
    ({"diagnosticInfo": False}, False),
    ({"diagnosticInfo": 0}, False),
    ({}, False),
)


@pytest.mark.parametrize("df_response,expected", detect_end_data)
def test_detect_end(df_response, expected):
    assert detect_end(df_response) == expected


response_to_question_data = (
    (
        True,
        "sleep.1",
        "en",
        "Congratulations, keep going because regularity of the time to get up is essential for a sleep of quality.",
    ),
    (
        False,
        "sleep.1",
        "en",
        "Regularity of the time to get up is essential for a sleep of quality. See the sleep chapter.",
    ),
    (
        True,
        "sleep.1",
        "es",
        "Felicidades, contin??a as?? porque la regularidad en la hora de levantarse es indispensable para un sue??o de calidad.",
    ),
    (
        False,
        "sleep.1",
        "es",
        "La regularidad en la hora de levantarse es indispensable para un sue??o de calidad. Consulta el cap??tulo del sue??o.",
    ),
    (
        True,
        "sleep.1",
        "fr",
        "F??licitions, continuez car la r??gularit?? de l???heure du lev?? est indispensable pour un sommeil de qualit??.",
    ),
    (
        False,
        "sleep.1",
        "fr",
        "La r??gularit?? de l???heure du lev?? est indispensable pour un sommeil de qualit??. Consultez le chapitre sommeil.",
    ),
    (
        True,
        "sleep.2",
        "en",
        "Well done! Persevere in keeping enough sleep each night, otherwise old problems may return ;-)",
    ),
    (
        False,
        "sleep.2",
        "en",
        "If you don't get enough sleep, you risk increasing your sleep deficit. See the sleep chapter.",
    ),
    (
        True,
        "sleep.2",
        "es",
        "??Bravo! Persevera en conservar una duraci??n suficiente de sue??o cada d??a, por el contrario, los viejos problemas podr??an volver ;-)",
    ),
    (
        False,
        "sleep.2",
        "es",
        "Si no duermes el tiempo suficiente, corres el riesgo de agravar tu d??ficit de sue??o. Consulta el cap??tulo del sue??o.",
    ),
    (
        True,
        "sleep.2",
        "fr",
        "Bravo! Pers??v??rez ?? conserver une dur??e suffisante de sommeil chaque nuit, sinon les anciens probl??mes peuvent revenir???;-)",
    ),
    (
        False,
        "sleep.2",
        "fr",
        "Si vous ne vous offrez pas un temps de sommeil suffisant, vous risquez de creuser votre d??ficit de sommeil. Consultez le chapitre sommeil.",
    ),
    (
        True,
        "sleep.5",
        "en",
        "Super good news! Stress is the number one enemy of restful sleep. Continue to anchor this habit by being rigorous in this practice for another 1 or 2 months. It will become as automatic as brushing your teeth!",
    ),
    (
        False,
        "sleep.5",
        "en",
        "Stress is the number one enemy of restful sleep. Explore the different ways to reduce your stress, if meditation isn't your cup of tea, for example try a good bath, reading, music or a nice walk in the evening. More ideas in the sleep chapter.",
    ),
    (
        True,
        "sleep.5",
        "es",
        "??S??per buena noticia! El estr??s es el primer enemigo de un sue??o reparador. Contin??a anclando este h??bito y siendo riguroso durante uno o dos meses m??s. ??Ser?? tan autom??tico como lavarte los dientes!",
    ),
    (
        False,
        "sleep.5",
        "es",
        "El estr??s es el primer enemigo del sue??o reparador. Explora los diferentes m??todos para reducir el estr??s, si la meditaci??n no es de tu agrado, trata, por ejemplo, de darte un buen ba??o, de leer, de escuchar m??sica por la noche. M??s ideas en el cap??tulo del sue??o.",
    ),
    (
        True,
        "sleep.5",
        "fr",
        "Super bonne nouvelle! Le stress est le premier ennemi d???un sommeil r??cup??rateur. Continuez ?? ancrer cette habitude en ??tant rigoureux sur cette pratique encore 1 mois ou 2. Cela deviendra aussi automatique que de vous brosser les dents!",
    ),
    (
        False,
        "sleep.5",
        "fr",
        "Le stress est le premier ennemi d???un sommeil r??cup??rateur. Explorez les diff??rentes m??thodes pour r??duire votre stress, si la m??ditation n???est pas votre tasse de th??, essayez par exemple un bon bain, de la lecture, de la musique ou une bonne balade le soir. Plus d???id??es dans le chapitre sommeil.",
    ),
)


@pytest.mark.parametrize(
    "user_msg,question_id,lang,expected",
    response_to_question_data,
    ids=range(len(response_to_question_data)),
)
def test_response_to_question(user_msg, question_id, lang, expected):
    question_response = QuestionResponse(
        user_response=user_msg, question_id=question_id
    )
    real = response_to_question(question_response, lang)
    assert real == expected
