"""Routes for manage bot conversations."""

from fastapi import APIRouter, Depends, Query

from app import crud
from app.api.dependencies.database import get_db
from app.api.dependencies.security import get_current_user
from app.core.bot import detect_intent_texts, fix_conversation, parse_parameters_field
from app.core.config import settings
from app.models import HealthData, User
from app.schemas.bot import Msg
from app.schemas.conversation import ConversationCreate
from app.schemas.health_data import HealthDataCreate, HealthDataUpdate

router = APIRouter()
algorithm = {
    "get_up": (
        "Congratulations, continue because the regularity of the time to get up is essential for a quality sleep.",
        "The regularity of the time to get up is essential for quality sleep. See the sleep chapter.",
    ),
    "sleep": (
        "Well done! Persevere in keeping enough sleep each night, otherwise the old problems may return ;-)",
        "If you don't get enough sleep, you risk increasing your sleep deficit. See the sleep chapter.",
    ),
    "screen": (
        "Compliment We realize that this is difficult. By avoiding screens you double the amount of deep sleep, the most restful every night ...",
        "Yep, it's not easy. We understand well. However, by avoiding screens you double the amount of deep sleep, the most recovering each night... See the sleep chapter.",
    ),
    "bedroom": (
        "It happened! Well done. These small changes greatly promote quality sleep.",
        "A cool, dark and quiet bedroom can greatly improve the quality of sleep. Wouldn't it be worth it? See the sleep chapter.",
    ),
    "stress": (
        "Super good news! Stress is the number one enemy of restful sleep. Continue to anchor this habit by being rigorous in this practice for another 1 or 2 months. It will become as automatic as brushing your teeth!",
        "Stress is the number one enemy of restful sleep. Explore the different ways to reduce your stress, if meditation is not your cup of tea, for example try a good bath, reading, music or a good walk in the evening. More ideas in the sleep chapter.",
    ),
}


@router.post("/process-msg", response_model=ConversationCreate)
def bot_message_post(
    *,
    db=Depends(get_db),
    input_pack: Msg,
    user: User = Depends(get_current_user),
    lang: str = Query("en"),
):
    """Sends a message to the bot and returns the response back."""

    health_data = None
    message = input_pack.msg

    response = detect_intent_texts(
        settings.dialogflow_project_id, user.id, message, lang
    )
    fulfillment_text = response.query_result.fulfillment_text

    intent = response.query_result.intent.display_name

    is_end = False
    try:
        if response.query_result.diagnostic_info:
            is_end = True
    except AttributeError:
        pass

    if response.query_result.parameters.fields:
        real = parse_parameters_field(response.query_result.parameters.fields)

        current_health_data = (
            db.query(HealthData).filter_by(valid=False, user_id=user.id).first()
        )
        real["user_id"] = user.id
        if current_health_data:
            health_data = HealthDataUpdate(**real, valid=is_end)
            crud.health_data.update(db, db_obj=current_health_data, obj_in=health_data)
        else:
            health_data = HealthDataCreate(**real, valid=is_end)
            crud.health_data.create(db, obj_in=health_data)

    conversation = ConversationCreate(
        user_msg=message, bot_msg=fulfillment_text, intent=intent, user_id=user.id
    )
    crud.conversation.create(db, obj_in=conversation)

    if health_data is not None:
        fix_conversation(conversation, health_data)

    return conversation
