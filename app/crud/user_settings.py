from typing import Optional
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

    def get_by_user_id(
        self, db: Session, *, user_id: int
    ) -> Optional[schemas.UserSettings]:
        return db.query(self.model).filter(self.model.user_id == user_id).first()

    def update(
        self, db: Session, update: schemas.UserSettingsUpdate, user_id: int
    ) -> schemas.UserSettings:
        settings = self.get_by_user_id(db, user_id=user_id)
        return super().update(db, db_obj=settings, obj_in=update)


user_settings = CRUDUserSettings(models.UserSettings)
