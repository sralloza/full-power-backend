from app.schemas.health_data import HealthDataCreate

from .utils import random_constrained_int


def gen_health_data_create(user_id: int, valid: bool):
    return HealthDataCreate(
        user_id=user_id,
        energy=random_constrained_int(1, 5),
        restful_sleep=random_constrained_int(1, 5),
        fall_asleep_easily=random_constrained_int(1, 5),
        deep_sleep=random_constrained_int(1, 5),
        enough_sleep=random_constrained_int(1, 5),
        energy_morning=random_constrained_int(1, 5),
        uniform_mood=random_constrained_int(1, 5),
        memory=random_constrained_int(1, 5),
        concentration=random_constrained_int(1, 5),
        creativity=random_constrained_int(1, 5),
        stress=random_constrained_int(1, 5),
        cramps=random_constrained_int(1, 5),
        dagger=random_constrained_int(1, 5),
        pump_strokes=random_constrained_int(1, 5),
        uplifts=random_constrained_int(1, 5),
        swollen_belly=random_constrained_int(1, 5),
        gases=random_constrained_int(1, 5),
        bowel_movement=random_constrained_int(1, 5),
        sheet_wipe=random_constrained_int(1, 5),
        bot_msg=random_constrained_int(1, 5),
        valid=valid,
    )
