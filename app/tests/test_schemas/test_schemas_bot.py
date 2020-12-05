import pytest
from pydantic import ValidationError

from app.schemas.bot import DFResponse, Msg


def test_msg():
    fields = Msg.__fields__
    assert set(fields) == {"msg"}

    assert fields["msg"].required == True
    assert fields["msg"].required == True

    with pytest.raises(ValidationError):
        Msg(msg="")

    Msg(msg="a")


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
