from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class HealthDataBase(BaseModel):
    energy: Optional[int]  # 1
    restful_sleep: Optional[int]  # 2
    fall_asleep_easily: Optional[int]  # 3
    deep_sleep: Optional[int]  # 4
    enough_sleep: Optional[int]  # 5
    energy_morning: Optional[int]  # 6

    uniform_mood: Optional[int]  # 7
    memory: Optional[int]  # 8
    concentration: Optional[int]  # 9
    creativity: Optional[int]  # 10
    stress: Optional[int]  # 11
    cramps: Optional[int]  # 12
    dagger: Optional[int]  # 13

    pump_strokes: Optional[int]  # 14
    uplifts: Optional[int]  # 15
    swollen_belly: Optional[int]  # 16
    gases: Optional[int]  # 17
    bowel_movement: Optional[int]  # 18
    sheet_wipe: Optional[int]  # 19

    timestamp: Optional[datetime]
    user_id: int
    valid: bool = False


class HealthDataCreate(HealthDataBase):
    pass


class HealthDataUpdate(HealthDataBase):
    pass


class HealthDataInDB(HealthDataBase):
    id: int

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True


class HealthData(HealthDataInDB):
    pass
