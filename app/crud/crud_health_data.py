import logging

from sqlalchemy.orm.session import Session

from app.models.health_data import HealthData
from app.schemas.health_data import HealthDataCreate, HealthDataUpdate

from .base import CRUDBase

logger = logging.getLogger(__name__)


class CRUDHealthData(CRUDBase[HealthData, HealthDataCreate, HealthDataUpdate]):
    def get_user(self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100):
        return (
            db.query(self.model)
            .filter_by(user_id=user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


health_data = CRUDHealthData(HealthData)
