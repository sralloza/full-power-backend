import random

from fastapi import APIRouter

from app.utils.translate import i18n

router = APIRouter(prefix="/notifications-content", tags=["notifications"])


@router.get(
    "/second-survey/{problem}",
    response_model=str,
    summary="Second survey notifications",
)
def get_second_survey_notifications(problem: str, lang: str):
    i18n.set("locale", lang)
    nchoices = int(i18n.t(f"notifications.{problem}.length"))
    messages = [
        i18n.t(f"notifications.{problem}.notif{i}") for i in range(1, nchoices + 1)
    ]
    return random.choice(messages)


@router.get("/generic", response_model=str, summary="Generic notifications")
def get_generic_notifications(lang: str):
    i18n.set("locale", lang)
    nchoices = int(i18n.t(f"notifications.generic.length"))
    messages = [
        i18n.t(f"notifications.generic.notif{i}") for i in range(1, nchoices + 1)
    ]
    return random.choice(messages)
