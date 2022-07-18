from datetime import datetime
from typing import List, Optional

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app import models, schemas

from .base import CRUDBase


class CRUDNote(CRUDBase[models.Note, schemas.NoteCreate, schemas.NoteUpdate]):
    class Errors:
        not_found_422 = {"loc": ["body", "id"], "msg": "Note not found."}

    def create(
        self, db: Session, *, note_in: schemas.NoteCreate, user_id: int
    ) -> schemas.Note:

        note = self.model(**note_in.dict(exclude_none=True), user_id=user_id)

        db.add(note)
        db.commit()
        db.refresh(note)

        return note

    def update(
        self, db: Session, *, id: int, update: schemas.NoteUpdate, user_id: int
    ) -> schemas.Note:
        note = self.get_by_id_and_user_id(db, id=id, user_id=user_id)

        edited_at = datetime.utcnow()
        note.edited_at = edited_at

        updated_note = super().update(db, db_obj=note, obj_in=update)
        return updated_note

    def get_multi(
        self,
        db: Session,
        *,
        user_id: int,
        search: Optional[str],
        skip: int = 0,
        limit: int = 100,
    ) -> List[schemas.Note]:
        q = db.query(self.model).filter(self.model.user_id == user_id)

        if search:
            q = q.filter(
                or_(
                    func.lower(self.model.label.contains(func.lower(search))),
                    func.lower(self.model.body.contains(func.lower(search))),
                )
            )

        notes = q.offset(skip).limit(limit).all()

        return notes

    def remove(self, db: Session, id: int, user_id: int) -> None:
        note = self.get_by_id_and_user_id(db, id=id, user_id=user_id)
        db.delete(note)
        db.commit()
        return

note = CRUDNote(models.Note)
