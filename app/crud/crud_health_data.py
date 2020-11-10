import logging

from app.models.health_data import HealthData
from app.schemas.health_data import HealthDataCreate, HealthDataUpdate

from .base import CRUDBase

logger = logging.getLogger(__name__)


class CRUDHealthData(CRUDBase[HealthData, HealthDataCreate, HealthDataUpdate]):
    pass


health_data = CRUDHealthData(HealthData)
