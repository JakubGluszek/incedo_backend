from sqlalchemy.orm import Session

from .base import CRUDBase
from app import models, schemas


class CRUDUserSettings(CRUDBase[models.UserSettings, None, schemas.UserSettingsUpdate]):
    def create(self, db: Session, *, user: schemas.User) -> schemas.UserSettings:
        settings = self.model(user_id=user.id)
        db.add(settings)
        db.commit()
        db.refresh(settings)
        return settings


user_settings = CRUDUserSettings(models.UserSettings)
