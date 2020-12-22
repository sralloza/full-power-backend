from json import dumps
from unittest import mock

import pytest
from pydantic import BaseModel, confloat

from app import crud
from app.core.health_data import hdprocessor
from app.schemas.bot import DFResponse
from app.schemas.conversation import Conversation, ConversationCreateResult, DisplayType
from app.schemas.health_data import HealthDataCreate
from app.tests.utils.user import get_normal_user_id

langs = list(hdprocessor.problem_result_text.dict().keys())


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
        class TempModel(BaseModel):
            problem: confloat(ge=0, le=1)

        self.get_df_res_m = mock.patch("app.api.routes.bot.get_df_response").start()
        self.phd_m = mock.patch(
            "app.api.routes.bot.hdprocessor.process_health_data"
        ).start()
        self.phd_m.return_value = TempModel(problem=1.0)
        self.irp_m = mock.patch(
            "app.api.routes.bot.hdprocessor.identify_real_problems"
        ).start()
        self.irp_m.return_value = "<problem>"
        yield
        mock.patch.stopall()

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
        conv = ConversationCreateResult(**response.json())

        assert conv.user_msg == "this is the user message"
        if not df_res.is_end:
            assert conv.bot_msg == "this is the bot message"
        else:
            assert conv.bot_msg == "this is the bot message. <problem>"
        assert conv.intent == "this is the intent"
        assert conv.display_type == DisplayType.default

        self.get_df_res_m.assert_called_once_with(mock.ANY, conv.user_msg, lang)

        convs_db = crud.conversation.get_multi(db)
        assert len(convs_db) >= 1
        conv_db = convs_db[-1]

        assert conv == ConversationCreateResult.parse_obj(
            Conversation.from_orm(conv_db)
        )

        if df_res.is_end:
            assert (
                response.headers["health-data-result"] == self.phd_m.return_value.json()
            )
            self.phd_m.assert_called_once_with(mock.ANY)
            self.irp_m.assert_called_once_with(self.phd_m.return_value, lang=lang)
        else:
            assert "health-data-result" not in response.headers
            self.phd_m.assert_not_called()
            self.irp_m.assert_not_called()

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
