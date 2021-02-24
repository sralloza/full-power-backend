import pytest

LANGS = ("en", "es", "fr")


@pytest.mark.parametrize("lang", LANGS)
def test_get_second_survey_notifications_ok(client, lang):
    responses = set()

    # Fail probability: (4/5) ** 100
    for _ in range(100):
        response = client.get(f"/notifications-content/second-survey/sleep?lang={lang}")
        assert response.status_code == 200

        data = response.json()
        new = tuple(data.items())
        if new not in responses:
            responses.add(new)

    assert len(responses) == 5


@pytest.mark.parametrize("lang", LANGS)
def test_get_second_survey_notifications_fail(client, lang):
    response = client.get(f"/notifications-content/second-survey/invalid?lang={lang}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid problem or lang"


@pytest.mark.parametrize("lang", LANGS)
def test_get_generic_notifications(client, lang):
    responses = set()

    # Fail probability: (2/3) ** 100
    for _ in range(100):
        response = client.get(f"/notifications-content/generic?lang={lang}")
        assert response.status_code == 200

        data = response.json()
        new = tuple(data.items())
        if new not in responses:
            responses.add(new)

    assert len(responses) == 3
