from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from .base import CRUDBase
from app import models, schemas, crud


class CRUDNote(CRUDBase[models.Note, schemas.NoteCreate, schemas.NoteUpdate]):
    class Errors:
        invalid_folder = {"loc": ["body", "folder_id"], "msg": "Invalid folder."}

    def create(
        self, db: Session, *, note_in: schemas.NoteCreate, user: schemas.User
    ) -> schemas.Note:

        # validate folder
        if note_in.folder_id:
            try:
                crud.notes_folder.get_by_id_and_user(db, id=note_in.folder_id, user=user)
            except HTTPException:
                raise HTTPException(
                    status_code=422, detail=[self.Errors.invalid_folder]
                )

        note = self.model(**note_in.dict(exclude_none=True), user_id=user.id)

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

        # validate folder
        if update.folder_id:
            try:
                crud.notes_folder.get_by_id_and_user(db, id=update.folder_id, user=user)
            except HTTPException:
                raise HTTPException(
                    status_code=422, detail=[self.Errors.invalid_folder]
                )

        updated_note = super().update(db, db_obj=note, obj_in=update)
        return updated_note

    def remove(self, db: Session, *, id: int, user: schemas.User) -> None:
        note = self.get(db, id)

        if not note or note.user_id != user.id:
            raise HTTPException(status_code=404)

        super().remove(db, id=id)
        return


note = CRUDNote(models.Note)
