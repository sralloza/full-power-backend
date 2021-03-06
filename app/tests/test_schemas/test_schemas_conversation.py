from typing import List

from app.schemas.conversation import (
    Conversation,
    ConversationCreate,
    ConversationCreateInner,
    ConversationCreateResult,
    ConversationInDB,
    ConversationOut,
    ConversationUpdate,
    DisplayType,
)


def test_display_type():
    assert DisplayType["default"] == DisplayType("default") == DisplayType.default
    assert (
        DisplayType["five_stars"] == DisplayType("five_stars") == DisplayType.five_stars
    )
    assert DisplayType["yes_no"] == DisplayType("yes_no") == DisplayType.yes_no


def test_conversation_create():
    fields = ConversationCreate.__fields__
    assert set(fields) == {"user_msg", "bot_msg", "intent", "user_id"}

    assert fields["user_msg"].required is True
    assert fields["user_msg"].type_ == str
    assert fields["bot_msg"].required is True
    assert fields["bot_msg"].type_ == str
    assert fields["intent"].required is True
    assert fields["intent"].type_ == str
    assert fields["user_id"].required is True
    assert fields["user_id"].type_ == int


def test_conversation_out():
    fields = ConversationOut.__fields__
    assert set(fields) == {"user_msg", "bot_msg", "intent", "user_id", "display_type"}

    assert fields["user_msg"].required is True
    assert fields["user_msg"].type_ == str
    assert fields["bot_msg"].required is True
    assert fields["bot_msg"].outer_type_ == List[str]
    assert fields["intent"].required is True
    assert fields["intent"].type_ == str
    assert fields["user_id"].required is True
    assert fields["user_id"].type_ == int
    assert fields["display_type"].required is True
    assert fields["display_type"].type_ == DisplayType

    assert ConversationCreateResult.__config__.orm_mode is True

    # Test validator
    conv = ConversationOut(
        user_msg="u",
        bot_msg="hi\nthere~everybody",
        intent="x",
        user_id=1,
        display_type="default",
    )
    assert conv.bot_msg == ["hi", "there", "everybody"]


def test_conversation_create_result():
    fields = ConversationCreateResult.__fields__
    assert set(fields) == {"user_msg", "bot_msg", "intent", "user_id", "display_type"}

    assert fields["user_msg"].required is True
    assert fields["user_msg"].type_ == str
    assert fields["bot_msg"].required is True
    assert fields["bot_msg"].type_ == str
    assert fields["intent"].required is True
    assert fields["intent"].type_ == str
    assert fields["user_id"].required is True
    assert fields["user_id"].type_ == int
    assert fields["display_type"].required is True
    assert fields["display_type"].type_ == DisplayType

    assert ConversationCreateResult.__config__.orm_mode is True


def test_conversation_create_inner():
    fields = ConversationCreateInner.__fields__
    assert set(fields) == set(ConversationCreateResult.__fields__)

    assert ConversationCreateInner.__config__.orm_mode is True


def test_conversation_update():
    fields = ConversationUpdate.__fields__
    assert set(fields) == {"user_msg", "bot_msg", "intent", "user_id"}

    assert fields["user_msg"].required is False
    assert fields["user_msg"].type_ == str
    assert fields["bot_msg"].required is False
    assert fields["bot_msg"].type_ == str
    assert fields["intent"].required is False
    assert fields["intent"].type_ == str
    assert fields["user_id"].required is False
    assert fields["user_id"].type_ == int


def test_conversation_in_db():
    fields = ConversationInDB.__fields__
    assert set(fields) == {
        "user_msg",
        "bot_msg",
        "intent",
        "user_id",
        "display_type",
        "id",
    }

    assert fields["user_msg"].required is True
    assert fields["user_msg"].type_ == str
    assert fields["bot_msg"].required is True
    assert fields["bot_msg"].type_ == str
    assert fields["intent"].required is True
    assert fields["intent"].type_ == str
    assert fields["user_id"].required is True
    assert fields["user_id"].type_ == int
    assert fields["display_type"].required is True
    assert fields["display_type"].type_ == DisplayType
    assert fields["id"].required == True
    assert fields["id"].type_ == int

    assert ConversationInDB.__config__.orm_mode is True


def test_conversation():
    fields = Conversation.__fields__
    assert set(fields) == {
        "user_msg",
        "bot_msg",
        "intent",
        "user_id",
        "display_type",
        "id",
    }

    assert fields["user_msg"].required is True
    assert fields["user_msg"].type_ == str
    assert fields["bot_msg"].required is True
    assert fields["bot_msg"].type_ == str
    assert fields["intent"].required is True
    assert fields["intent"].type_ == str
    assert fields["user_id"].required is True
    assert fields["user_id"].type_ == int
    assert fields["display_type"].required is True
    assert fields["display_type"].type_ == DisplayType
    assert fields["id"].required == True
    assert fields["id"].type_ == int

    assert ConversationInDB.__config__.orm_mode is True
