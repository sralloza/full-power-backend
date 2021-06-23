import random

from fastapi import APIRouter, HTTPException

from app.schemas.notification import QuestionNotification
from app.utils.responses import gen_responses
from app.utils.translate import i18n

router = APIRouter(prefix="/notifications-content", tags=["Notifications"])


@router.get(
    "/second-survey/{problem}",
    response_description="Notification content",
    response_model=QuestionNotification,
    summary="Second survey notifications",
    **gen_responses({400: "Invalid problem or language"}),
)
def get_second_survey_notifications(problem: str, lang: str):
    """Returns a random question from the second survey questions."""
    i18n.set("locale", lang)

    try:
        nchoices = int(i18n.t(f"notifications.{problem}.length"))
        choice = random.randint(1, nchoices)

        return QuestionNotification(
            content=i18n.t(f"notifications.{problem}.notif{choice}"),
            id=f"{problem}.{choice}",
        )
    except KeyError:
        raise HTTPException(400, "Invalid problem or lang")


@router.get(
    "/generic",
    response_description="Notification content",
    response_model=QuestionNotification,
    summary="Generic notifications",
)
def get_generic_notifications(lang: str):
    """Returns a random generic notification."""

    i18n.set("locale", lang)
    nchoices = int(i18n.t("notifications.generic.length"))
    choice = random.randint(1, nchoices)

    return QuestionNotification(
        content=i18n.t(f"notifications.generic.notif{choice}"),
        id=f"generic.{choice}",
    )
