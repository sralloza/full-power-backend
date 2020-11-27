from app.schemas.bot import DFResponse
from unittest import mock
import pytest
from app.core.bot import detect_end, get_df_response, parse_df_response
import dialogflow


class TestGetDFResonse:
    @pytest.fixture(autouse=True)
    def mocks(self):
        self.client_m = mock.patch("dialogflow.SessionsClient").start()
        mock.patch("app.core.bot.settings.dialogflow_project_id", 600).start()
        self.mtd_m = mock.patch("app.core.bot.MessageToDict").start()
        self.parse_df_response_m = mock.patch("app.core.bot.parse_df_response").start()
        yield
        mock.patch.stopall()

    def test_get_df_response(self):
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
