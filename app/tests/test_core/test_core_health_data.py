from itertools import product
from unittest import mock

import numpy as np
import pytest
from fastapi import HTTPException

from app.core.health_data import coefficients, detect_main_problem
from app.core.health_data import problem_names as columns_out
from app.core.health_data import problem_text, process_health_data
from app.schemas.health_data import HealthDataCreate
from app.tests.utils.utils import random_int

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

problems = (
    "Tu principal problema es vitaminas",
    "Your main problem is vitamines",
    "votre problème principal est vitamines",
    "Tu principal problema es dormir",
    "Your main problem is sleep",
    "votre problème principal est sommeil",
    "Tu principal problema es alimentación",
    "Your main problem is diet",
    "votre problème principal est alimentation",
    "Tu principal problema es estrés",
    "Your main problem is stress",
    "votre problème principal est stress",
)
columns_in = list(coefficients.keys())
langs = list(problem_text.keys())


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
    return {k: request.param[i] for i, k in enumerate(columns_out)}


@pytest.mark.parametrize(
    "health_data_in,data_out",
    zip(test_process_data_in, test_process_data_out),
    indirect=True,
)
def test_process_health_data(health_data_in, data_out):
    result = process_health_data(health_data_in)
    result = {key: round(value, 5) for key, value in result.items()}
    assert result == data_out


def test_process_health_data_error(caplog):
    caplog.set_level(10)
    health_data = HealthDataCreate(user_id=2)
    with pytest.raises(HTTPException) as exc_info:
        process_health_data(health_data)

    exc = exc_info.value
    assert exc.status_code == 500
    assert exc.detail == "Fatal error processing health data"

    assert caplog.record_tuples == [
        (mock.ANY, 40, f"Found error processing health data ({health_data!r})")
    ]


detect_main_problem_data = list(
    zip(list(product(test_process_data_out, langs)), problems)
)
detect_main_problem_data = ((*x[0], x[1]) for x in detect_main_problem_data)


@pytest.mark.parametrize(
    "data_out, lang, problem", detect_main_problem_data, indirect=["data_out"]
)
def test_detect_main_problem(data_out, problem, lang):
    assert detect_main_problem(data_out, lang) == problem
