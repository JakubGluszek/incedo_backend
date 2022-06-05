from typing import List
from fastapi import HTTPException
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

    def get_multi(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[schemas.Note]:
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(
        self, db: Session, *, id: int, update: schemas.NoteUpdate, user: schemas.User
    ) -> schemas.Note:
        note = self.get(db, id)

        if not note or note.user_id != user.id:
            raise HTTPException(status_code=404)

        updated_note = super().update(db, db_obj=note, obj_in=update)
        return updated_note

    def remove(self, db: Session, *, id: int, user: schemas.User) -> None:
        note = self.get(db, id)
        
        if not note or note.user_id != user.id:
            raise HTTPException(status_code=404)
        
        super().remove(db, id=id)
        return


note = CRUDNote(models.Note)
