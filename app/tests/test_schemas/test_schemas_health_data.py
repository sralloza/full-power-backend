from datetime import datetime

import pytest
from pydantic import ValidationError

from app.schemas.health_data import (
    HealthData,
    HealthDataCreate,
    HealthDataInDB,
    HealthDataProccessResult,
    HealthDataUpdate,
    QuestionCoefficients,
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


def test_question_coefficients():
    fields = QuestionCoefficients.__fields__
    assert set(fields) == {"question_id", "vitamins", "sleep", "diet", "stress"}

    assert fields["question_id"].required is True
    assert fields["question_id"].type_ == str
    assert issubclass(fields["vitamins"].type_, int)
    assert fields["sleep"].required is True
    assert issubclass(fields["sleep"].type_, int)
    assert fields["diet"].required is True
    assert issubclass(fields["diet"].type_, int)
    assert fields["stress"].required is True
    assert issubclass(fields["stress"].type_, int)

    with pytest.raises(ValidationError):
        QuestionCoefficients(**{x: -5 for x in fields})

    QuestionCoefficients(**{x: 0 for x in fields})
    QuestionCoefficients(**{x: 1 for x in fields})


def test_health_data_process_result():
    fields = HealthDataProccessResult.__fields__
    assert set(fields) == {"vitamins", "sleep", "diet", "stress"}

    assert fields["vitamins"].required is True
    assert issubclass(fields["vitamins"].type_, float)
    assert fields["sleep"].required is True
    assert issubclass(fields["sleep"].type_, float)
    assert fields["diet"].required is True
    assert issubclass(fields["diet"].type_, float)
    assert fields["stress"].required is True
    assert issubclass(fields["stress"].type_, float)

    with pytest.raises(ValidationError):
        HealthDataProccessResult(**{x: 5 for x in fields})
    with pytest.raises(ValidationError):
        HealthDataProccessResult(**{x: -5 for x in fields})

    HealthDataProccessResult(**{x: 0 for x in fields})
    HealthDataProccessResult(**{x: 0.5 for x in fields})
    HealthDataProccessResult(**{x: 1 for x in fields})


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
