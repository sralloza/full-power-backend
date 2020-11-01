import pytest
from fastapi.testclient import TestClient

from app.main import create_app


def test_fatal_error(caplog):
    caplog.set_level(10)
    app = create_app()

    @app.get("/error")
    def raise_error():
        raise ValueError

    assert raise_error
    client = TestClient(app)
    with pytest.raises(ValueError):
        client.get("/error")

    assert len(caplog.records) == 1
    record = caplog.records[0]

    assert record.levelname == "CRITICAL"
    assert "[testclient]" in record.args[1]
