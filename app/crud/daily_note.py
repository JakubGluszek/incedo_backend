from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from .base import CRUDBase
from app import models, schemas


class CRUDDailyNote(
    CRUDBase[models.DailyNote, schemas.DailyNoteCreate, schemas.DailyNoteUpdate]
):
    def create(
        self, db: Session, *, note_in: schemas.DailyNoteCreate, user: schemas.User
    ) -> schemas.DailyNote:

        if user.settings.time_diff:
            date = datetime.utcnow() + timedelta(hours=user.settings.time_diff)
        else:
            date = datetime.utcnow()

        note = self.model(**note_in.dict(), date=date, user_id=user.id)

        db.add(note)
        db.commit()
        db.refresh(note)

        return note

    def get_by_date(
        self, db: Session, date: datetime, user: schemas.User
    ) -> Optional[schemas.DailyNote]:
        return (
            db.query(self.model)
            .filter(
                self.model.user_id == user.id,
                func.date(self.model.date) == func.date(date),
            )
            .first()
        )

    def get_todays(self, db: Session, user: schemas.User) -> schemas.DailyNote:
        if user.settings.time_diff:
            date = datetime.utcnow() + timedelta(hours=user.settings.time_diff)
        else:
            date = datetime.utcnow()

        note = (
            db.query(self.model)
            .filter(
                self.model.user_id == user.id,
                func.date(self.model.date) == func.date(date),
            )
            .first()
        )
        if not note:
            raise HTTPException(status_code=404)
        return note

    def get_multi(
        self, db: Session, *, user: schemas.User, skip: int = 0, limit: int = 100
    ) -> List[schemas.DailyNote]:
        return (
            db.query(self.model)
            .filter(self.model.user_id == user.id)
            .offset(skip)
            .limit(limit)
            .all()
        )


daily_note = CRUDDailyNote(models.DailyNote)
