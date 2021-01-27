import pytest

from app.utils.bot import split_bot_msg


@pytest.mark.parametrize(
    "bot_msg,frontend_msg",
    (("a\nb~c", ["a", "b", "c"]), ("a~b\nc", ["a", "b", "c"])),
)
def test_split_bot_msg(bot_msg, frontend_msg):
    result = split_bot_msg(bot_msg)
    assert result == frontend_msg
