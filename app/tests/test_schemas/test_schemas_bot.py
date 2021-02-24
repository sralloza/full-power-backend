import pytest
from pydantic import ValidationError

from app.schemas.bot import DFResponse, QuestionResponse


def test_dialogflow_response():
    fields = DFResponse.__fields__
    assert set(fields) == {"bot_msg", "intent", "is_end", "parameters"}

    assert fields["bot_msg"].required is True
    assert fields["bot_msg"].type_ == str
    assert fields["intent"].required is True
    assert fields["intent"].type_ == str
    assert fields["is_end"].required is True
    assert fields["is_end"].type_ == bool
    assert fields["parameters"].required is True
    assert fields["parameters"].type_ == dict

    DFResponse(
        bot_msg="bot", intent="intent", is_end=True, parameters=dict(key="value")
    )


def test_question_response():
    fields = QuestionResponse.__fields__
    assert set(fields) == {"user_response", "question_id"}

    assert fields["user_response"].required is True
    assert fields["question_id"].required is True
    assert fields["user_response"].type_ == bool
    assert fields["question_id"].type_ == str

    QuestionResponse(user_response=True, question_id="sleep.1")
    with pytest.raises(ValidationError):
        QuestionResponse(user_response=True, question_id="invalid")
    with pytest.raises(ValidationError):
        QuestionResponse(user_response=True, question_id="invalid.1")
    with pytest.raises(ValidationError):
        QuestionResponse(user_response=True, question_id="sleep.0")
    with pytest.raises(ValidationError):
        QuestionResponse(user_response=True, question_id="sleep.9999")
