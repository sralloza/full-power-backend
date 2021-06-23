from unittest import mock

import pytest

from app import crud
from app.core.config import settings
from app.schemas.bot import DFResponse
from app.schemas.conversation import Conversation, ConversationOut, DisplayType
from app.schemas.health_data import (
    ClassifiedProblemList,
    HealthDataCreate,
    HealthDataProccessResult,
)
from app.tests.utils.user import get_normal_user_id

langs = ("en", "es", "fr")


class TestProcessMsg:
    responses = (
        DFResponse(
            bot_msg="this is the bot message",
            intent="this is the intent",
            is_end=False,
            parameters={},
            user_msg="this is the user message",
        ),
        DFResponse(
            bot_msg="this is the bot message",
            intent="this is the intent",
            is_end=False,
            parameters={"dagger": 4},
            user_msg="this is the user message",
        ),
        DFResponse(
            bot_msg="this is the bot message",
            intent="this is the intent",
            is_end=True,
            parameters={"sheet_wipe": 1},
            user_msg="this is the user message",
        ),
    )

    @pytest.fixture(autouse=True)
    def mocks(self):
        self.rtq_m = mock.patch("app.api.routes.bot.response_to_question").start()
        self.rtq_m.return_value = "<question-response>"
        self.get_df_res_m = mock.patch("app.api.routes.bot.get_df_response").start()
        self.phd_m = mock.patch(
            "app.api.routes.bot.hdprocessor.process_health_data"
        ).start()
        self.phd_m.return_value = HealthDataProccessResult(
            vitamins=0.5,
            sleep=0.5,
            diet=0.5,
            stress=0.5,
        )
        self.cp_m = mock.patch(
            "app.api.routes.bot.hdprocessor.classify_problems"
        ).start()
        self.cp_m.return_value = ClassifiedProblemList(
            __root__=[{"name": "vitamins", "severity": "serious"}]
        )
        self.gr_m = mock.patch("app.api.routes.bot.hdprocessor.gen_report").start()
        self.gr_m.return_value = "<problem>"
        yield
        mock.patch.stopall()

    def test_no_args(self, client, normal_user_token_headers):
        response = client.post(
            "/bot/process-msg?lang=en", headers=normal_user_token_headers
        )
        assert response.status_code == 400
        detail = response.json()["detail"]
        assert detail == "You need to pass 'msg' or 'question_response'"

        self.get_df_res_m.assert_not_called()

    def test_both_args(self, client, normal_user_token_headers):
        response = client.post(
            "/bot/process-msg?lang=en",
            headers=normal_user_token_headers,
            json={
                "msg": "this is the user message",
                "question_response": {"user_response": True, "question_id": "sleep.1"},
            },
        )
        assert response.status_code == 400
        detail = response.json()["detail"]
        assert detail == "'msg' and 'question_response' are mutually exlusive"

        self.get_df_res_m.assert_not_called()

    def test_response_to_question(self, client, normal_user_token_headers):
        response = client.post(
            "/bot/process-msg?lang=en",
            json={
                "question_response": {"user_response": True, "question_id": "sleep.1"}
            },
            headers=normal_user_token_headers,
        )
        assert response.status_code == 200
        data = response.json()

        assert data["display_type"] == "default"
        assert data["bot_msg"] == ["<question-response>"]
        assert data["intent"] == "notification-question-response"
        assert data["user_msg"] == "True"

        self.rtq_m.assert_called_once_with(mock.ANY, "en")
        self.get_df_res_m.assert_not_called()

    def test_ask_question(self, client, normal_user_token_headers):
        response = client.post(
            "/bot/process-msg?lang=en",
            json={"msg": settings.bot_question_message_flag + "this is the question"},
            headers=normal_user_token_headers,
        )
        assert response.status_code == 200
        data = response.json()

        assert data["display_type"] == "yes_no"
        assert data["bot_msg"] == ["this is the question"]
        assert data["intent"] == "notification-question-echo"
        assert data["user_msg"] == "this is the question"

        self.rtq_m.assert_not_called()
        self.get_df_res_m.assert_not_called()

    @pytest.mark.parametrize("df_res", responses)
    @pytest.mark.parametrize("lang", langs)
    def test_process_msg(self, df_res, lang, client, db, normal_user_token_headers):
        self.get_df_res_m.return_value = df_res.copy()
        if df_res.is_end:
            crud.health_data.create(
                db, obj_in=HealthDataCreate(user_id=get_normal_user_id(db))
            )

        response = client.post(
            f"/bot/process-msg?lang={lang}",
            json={"msg": "this is the user message"},
            headers=normal_user_token_headers,
        )
        assert response.status_code == 200
        conv = ConversationOut(**response.json())

        assert conv.user_msg == "this is the user message"
        if not df_res.is_end:
            assert conv.bot_msg == ["this is the bot message"]
            assert response.json()["bot_msg"] == "this is the bot message"
        else:
            assert conv.bot_msg == ["this is the bot message", "<problem>"]
            assert response.json()["bot_msg"] == "this is the bot message <problem>"

        assert conv.intent == "this is the intent"
        assert conv.display_type == DisplayType.default

        self.get_df_res_m.assert_called_once_with(mock.ANY, conv.user_msg, lang)

        convs_db = crud.conversation.get_multi(db)
        assert len(convs_db) >= 1
        conv_db = convs_db[-1]

        assert conv == ConversationOut.parse_obj(Conversation.from_orm(conv_db))

        if df_res.is_end:
            headers = response.headers
            assert headers["X-Problems-Parsed"] == self.cp_m.return_value.json()
            assert headers["X-Health-Data-Result"] == self.phd_m.return_value.json()

            self.phd_m.assert_called_once_with(mock.ANY)
            self.cp_m.assert_called_once_with(self.phd_m.return_value)
            self.gr_m.assert_called_once_with(self.cp_m.return_value, lang=lang)
        else:
            assert "health-data-result" not in response.headers
            self.phd_m.assert_not_called()
            self.cp_m.assert_not_called()
            self.gr_m.assert_not_called()

    @pytest.mark.parametrize("lang", langs)
    def test_error(self, db, client, normal_user_token_headers, lang):
        assert len(crud.health_data.get_multi(db)) == 0
        assert len(crud.conversation.get_multi(db)) == 0

        df_res = self.responses[-1]
        self.get_df_res_m.return_value = df_res.copy()
        response = client.post(
            f"/bot/process-msg?lang={lang}",
            json={"msg": "this is the user message"},
            headers=normal_user_token_headers,
        )

        assert response.status_code == 500
        assert response.json()["detail"] == "HealthData was not saved before processing"
