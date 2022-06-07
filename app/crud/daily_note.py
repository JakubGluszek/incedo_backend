from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from .base import CRUDBase
from app import models, schemas


class CRUDDailyNote(
    CRUDBase[models.DailyNote, schemas.DailyNoteCreate, schemas.DailyNoteUpdate]
):
    def create(
        self, db: Session, *, note_in: schemas.DailyNoteCreate, user: schemas.User
    ) -> schemas.DailyNote:

        date = datetime.utcnow() + timedelta(hours=0)  # TODO - user.timezone diff here
        note = self.model(**note_in.dict(), date=date, user_id=user.id)

        db.add(note)
        db.commit()
        db.refresh(note)

        return note


daily_note = CRUDDailyNote(models.DailyNote)
