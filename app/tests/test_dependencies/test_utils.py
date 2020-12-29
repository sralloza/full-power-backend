from app.api.dependencies.utils import get_limits
from inspect import signature


def test_get_limits():
    sig = signature(get_limits)
    assert list(sig.parameters) == ["skip", "limit"]
    assert sig.parameters["skip"].annotation == int
    assert sig.parameters["limit"].annotation == int
    assert sig.parameters["skip"].default == 0
    assert sig.parameters["limit"].default == 100
