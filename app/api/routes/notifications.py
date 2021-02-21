import random

from fastapi import APIRouter

from app.schemas.notification import QuestionNotification
from app.utils.translate import i18n

router = APIRouter(prefix="/notifications-content", tags=["notifications"])


@router.get(
    "/second-survey/{problem}",
    response_model=QuestionNotification,
    summary="Second survey notifications",
)
def get_second_survey_notifications(problem: str, lang: str):
    # TODO: test that problem exists
    # TODO: test that lang exists
    i18n.set("locale", lang)
    nchoices = int(i18n.t(f"notifications.{problem}.length"))
    choice = random.randint(1, nchoices)
    return QuestionNotification(
        content=i18n.t(f"notifications.{problem}.notif{choice}"),
        id=f"{problem}.{choice}",
    )


@router.get("/generic", response_model=QuestionNotification, summary="Generic notifications")
def get_generic_notifications(lang: str):
    # TODO: test that lang exists
    i18n.set("locale", lang)
    nchoices = int(i18n.t(f"notifications.generic.length"))
    choice = random.randint(1, nchoices)
    return QuestionNotification(
        content=i18n.t(f"notifications.generic.notif{choice}"),
        id=f"generic.{choice}",
    )
