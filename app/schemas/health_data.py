from typing import Optional

from pydantic import BaseModel


class HealthDataCreate(BaseModel):
    get_up: Optional[bool]
    sleep: Optional[bool]
    screen: Optional[bool]
    bedroom: Optional[bool]
    stress: Optional[bool]
    user_id: int
    valid: bool = False


class HealthDataUpdate(HealthDataCreate):
    pass
