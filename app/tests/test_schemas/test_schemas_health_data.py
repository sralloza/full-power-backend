from datetime import datetime

from app.schemas.health_data import (
    HealthData,
    HealthDataCreate,
    HealthDataInDB,
    HealthDataUpdate,
)

questions_fields = {
    "energy",
    "restful_sleep",
    "fall_asleep_easily",
    "deep_sleep",
    "enough_sleep",
    "energy_morning",
    "uniform_mood",
    "memory",
    "concentration",
    "creativity",
    "stress",
    "cramps",
    "dagger",
    "pump_strokes",
    "uplifts",
    "swollen_belly",
    "gases",
    "bowel_movement",
    "sheet_wipe",
}


def test_health_data_create():
    fields = HealthDataCreate.__fields__
    assert set(fields) == questions_fields | {"timestamp", "user_id", "valid"}

    for field in questions_fields:
        assert fields[field].required is False
        assert fields[field].type_ == int

    assert fields["timestamp"].required is False
    assert fields["timestamp"].type_ == datetime
    assert fields["user_id"].required is True
    assert fields["user_id"].type_ == int
    assert fields["valid"].required is False
    assert fields["valid"].default is False
    assert fields["valid"].type_ == bool


def test_health_data_update():
    fields = HealthDataUpdate.__fields__
    assert set(fields) == questions_fields | {"timestamp", "valid"}

    for field in questions_fields:
        assert fields[field].required is False
        assert fields[field].type_ == int

    assert fields["timestamp"].required is False
    assert fields["timestamp"].type_ == datetime
    assert fields["valid"].required is False
    assert fields["valid"].default is False
    assert fields["valid"].type_ == bool


def test_health_data_in_db():
    fields = HealthDataInDB.__fields__
    assert set(fields) == questions_fields | {"timestamp", "user_id", "valid", "id"}

    for field in questions_fields:
        assert fields[field].required is False
        assert fields[field].type_ == int

    assert fields["timestamp"].required is False
    assert fields["timestamp"].type_ == datetime
    assert fields["user_id"].required is True
    assert fields["user_id"].type_ == int
    assert fields["valid"].required is False
    assert fields["valid"].default is False
    assert fields["valid"].type_ == bool
    assert fields["id"].required is True
    assert fields["id"].type_ == int

    assert HealthDataInDB.__config__.orm_mode is True


def test_health_data():
    fields = HealthData.__fields__
    assert set(fields) == questions_fields | {"timestamp", "user_id", "valid", "id"}

    for field in questions_fields:
        assert fields[field].required is False
        assert fields[field].type_ == int

    assert fields["timestamp"].required is False
    assert fields["timestamp"].type_ == datetime
    assert fields["user_id"].required is True
    assert fields["user_id"].type_ == int
    assert fields["valid"].required is False
    assert fields["valid"].default is False
    assert fields["valid"].type_ == bool
    assert fields["id"].required is True
    assert fields["id"].type_ == int

    assert HealthDataInDB.__config__.orm_mode is True
