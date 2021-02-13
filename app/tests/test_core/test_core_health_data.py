from copy import deepcopy
from pathlib import Path
from typing import List
from unittest import mock

import numpy as np
import pytest
from fastapi import HTTPException
from pydantic import BaseModel, parse_file_as, parse_obj_as, validator

from app.core.health_data import Problem, hdprocessor
from app.schemas.health_data import (
    HealthDataCreate,
    HealthDataProccessResult,
    QuestionCoefficients,
)
from app.tests.utils.utils import random_int


def test_hdprocessor_attrs():
    from app.core.health_data import _HealthDataProcessor

    assert isinstance(hdprocessor, _HealthDataProcessor)
    assert hasattr(hdprocessor, "question_coeffs")
    assert hasattr(hdprocessor, "sums")


def test_sum_coefficients():
    new_hdprocessor = deepcopy(hdprocessor)
    unparsed_data = [
        {"vitamins": 7, "sleep": 3, "diet": 6, "stress": 8, "question_id": "#1"},
        {"vitamins": 3, "sleep": 8, "diet": 10, "stress": 1, "question_id": "#2"},
        {"vitamins": 7, "sleep": 7, "diet": 9, "stress": 3, "question_id": "#3"},
    ]
    coeffs = parse_obj_as(List[QuestionCoefficients], unparsed_data)
    new_hdprocessor.question_coeffs = coeffs

    expected = {"vitamins": 68, "sleep": 72, "diet": 100, "stress": 48}
    assert new_hdprocessor._sum_coefficients() == expected


test_process_data_in = (
    "0 4 4 3 4 2 2 0 3 2 4 0 0 4 4 3 2 1 3",
    "2 0 1 1 0 1 4 4 4 0 0 4 4 4 4 4 4 4 4",
    "1 4 2 1 3 0 4 0 4 4 4 2 3 2 3 1 0 2 4",
    "2 4 3 1 4 0 1 2 0 4 0 3 0 1 0 2 3 4 2",
)
test_process_data_out = (
    (0.50000, 0.12500, 0.29167, 0.37500),
    (0.47917, 0.87500, 0.00000, 0.50000),
    (0.39583, 0.41667, 0.50000, 0.04167),
    (0.58333, 0.33333, 0.50000, 0.79167),
)

columns_in = [x.question_id for x in hdprocessor.question_coeffs]


@pytest.fixture
def health_data_in(request):
    data_in = np.fromstring(request.param, sep=" ")

    # data_in is generated from excel file in scale 0-4. We need to
    # add 1 to convert to our scale (1-5)
    data_in = {k: data_in[i] + 1 for i, k in enumerate(columns_in)}

    user_id = random_int()
    health_data = HealthDataCreate(**data_in, valid=True, user_id=user_id)
    return health_data


@pytest.fixture
def data_out(request):
    return {k: request.param[i] for i, k in enumerate(hdprocessor.problem_names)}


@pytest.mark.parametrize(
    "health_data_in,data_out",
    zip(test_process_data_in, test_process_data_out),
    indirect=True,
)
def test_process_health_data(health_data_in, data_out):
    result = hdprocessor.process_health_data(health_data_in)
    result = {key: round(value, 5) for key, value in result}
    assert result == data_out


def test_process_health_data_error(caplog):
    caplog.set_level(10)
    health_data = HealthDataCreate(user_id=2)
    with pytest.raises(HTTPException) as exc_info:
        hdprocessor.process_health_data(health_data)

    exc = exc_info.value
    assert exc.status_code == 500
    assert exc.detail == "Fatal error processing health data"

    assert caplog.record_tuples == [
        (mock.ANY, 40, f"Found error processing health data ({health_data!r})")
    ]


class IRPTestData(BaseModel):
    result: HealthDataProccessResult
    problems: List[Problem]

    @validator("problems", pre=True)
    def check_problems(cls, v):
        if isinstance(v, list) and v and isinstance(v[0], str):  # noqa
            return [Problem(*x.split("-")) for x in v]


cp_test_data_path = Path(__file__).parent.parent / "test_data/problems_data.json"
classify_problems_test_data = parse_file_as(List[IRPTestData], cp_test_data_path)


@pytest.mark.parametrize("test_data", classify_problems_test_data)
def test_classify_problems(test_data: IRPTestData):
    real = hdprocessor.classify_problems(test_data.result)
    assert real == test_data.problems


class GenReportTestData(BaseModel):
    name: str
    inputs: List[List[str]]
    outputs: str
    lang: str

    @validator("inputs", pre=True)
    def check_inputs(cls, v):
        if isinstance(v, list) and v and isinstance(v[0], str):
            return [x.split("-") for x in v]
        return v


gr_test_data_path = Path(__file__).parent.parent / "test_data/gen_report.json"
gen_report_test_data = parse_file_as(List[GenReportTestData], gr_test_data_path)
ids = [f"{x.name}-{x.lang}" for x in gen_report_test_data]
gen_report_test_data = [(x.inputs, x.outputs, x.lang) for x in gen_report_test_data]


@pytest.mark.parametrize("inputs, outputs, lang", gen_report_test_data, ids=ids)
def test_gen_report(inputs, outputs, lang):
    inputs = [Problem(*x) for x in inputs]
    real = hdprocessor.gen_report(inputs, lang=lang)
    assert real == outputs
