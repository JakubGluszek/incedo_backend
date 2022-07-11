from sqlalchemy.orm import Session

from .base import CRUDBase
from app import schemas, models


class CRUDTheme(CRUDBase[models.Theme, schemas.ThemeCreate, schemas.ThemeUpdate]):
    def create(
        self, db: Session, theme_in: schemas.ThemeCreate, user_id: int
    ) -> schemas.Theme:
        theme = self.model(**theme_in.dict(), user_id=user_id)
        db.add(theme)
        db.commit()
        db.refresh(theme)
        return theme

    def update(
        self, db: Session, *, id: int, update: schemas.ThemeUpdate, user_id: int
    ) -> schemas.Theme:
        theme = self.get_by_id_and_user_id(db, id=id, user_id=user_id)
        updated = super().update(db, db_obj=theme, obj_in=update)
        return updated

    def remove(self, db: Session, *, id: int, user_id: int) -> None:
        theme = self.get_by_id_and_user_id(db, id=id, user_id=user_id)
        super().remove(db, theme.id)
        return


theme = CRUDTheme(models.Theme)
