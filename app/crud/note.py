from sqlalchemy.orm import Session

from .base import CRUDBase
from app import models, schemas


class CRUDNote(CRUDBase[models.Note, schemas.NoteCreate, schemas.NoteUpdate]):
    def create(
        self, db: Session, *, note_in: schemas.NoteCreate, user: schemas.User
    ) -> schemas.Note:

        note = self.model(**note_in.dict(), user_id=user.id)

        db.add(note)
        db.commit()
        db.refresh(note)

        return note


note = CRUDNote(models.Note)
