from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, confloat, conint
from typing_extensions import Literal


class ClassifiedProblem(BaseModel):
    name: str
    severity: Literal["light", "serious"]


class ClassifiedProblemList(BaseModel):
    __root__: List[ClassifiedProblem]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]

class QuestionCoefficients(BaseModel):
    question_id: str
    vitamins: conint(ge=0)
    sleep: conint(ge=0)
    diet: conint(ge=0)
    stress: conint(ge=0)


class HealthDataProccessResult(BaseModel):
    vitamins: confloat(ge=0, le=1)
    sleep: confloat(ge=0, le=1)
    diet: confloat(ge=0, le=1)
    stress: confloat(ge=0, le=1)


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
    valid: bool = False


class HealthDataCreate(HealthDataBase):
    user_id: int


class HealthDataUpdate(HealthDataBase):
    valid: Optional[bool] = False


class HealthDataInDB(HealthDataCreate):
    id: int

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True


class HealthData(HealthDataInDB):
    pass
