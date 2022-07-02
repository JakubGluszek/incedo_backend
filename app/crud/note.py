from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from .base import CRUDBase
from app import models, schemas, crud


class CRUDNote(CRUDBase[models.Note, schemas.NoteCreate, schemas.NoteUpdate]):
    class Errors:
        no_notebook = {"loc": ["body", "notebook_id"], "msg": "Notebook not found"}
        not_found_422 = {"loc": ["body", "id"], "msg": "Note not found."}

    def create(
        self, db: Session, *, note_in: schemas.NoteCreate, user_id: int
    ) -> schemas.Note:
        # validate notebook
        try:
            notebook = crud.notebook.get_by_id_and_user_id(
                db, id=note_in.notebook_id, user_id=user_id
            )
        except HTTPException:
            raise HTTPException(status_code=422, detail=[self.Errors.no_notebook])

        rank = self.generate_rank(db, notebook_id=notebook.id)

        if not note_in.label:
            note_in.label = f"Note {rank + 1}"

        note = self.model(**note_in.dict(exclude_none=True), user_id=user_id, rank=rank)

        notebook.edited_at = datetime.utcnow()
        db.add(notebook)
        db.add(note)
        db.commit()
        db.refresh(note)

        return note

    def update(
        self, db: Session, *, id: int, update: schemas.NoteUpdate, user_id: int
    ) -> schemas.Note:
        note = self.get(db, id)
        if not note or note.user_id != user_id:
            raise HTTPException(status_code=404)

        # validate notebook
        if update.notebook_id:
            try:
                notebook = crud.notebook.get_by_id_and_user_id(
                    db, id=update.notebook_id, user_id=user_id
                )
            except HTTPException:
                raise HTTPException(status_code=422, detail=[self.Errors.no_notebook])
        else:
            notebook = crud.notebook.get_by_id_and_user_id(
                db, id=note.notebook_id, user_id=user_id
            )

        edited_at = datetime.utcnow()

        notebook.edited_at = edited_at
        note.edited_at = edited_at

        db.add(notebook)

        updated_note = super().update(db, db_obj=note, obj_in=update)
        return updated_note

    def get_multi(
        self,
        db: Session,
        *,
        user_id: int,
        search: Optional[str],
        sort: Optional[str],
        order: Optional[str],
        orphaned: bool = False,
        skip: int = 0,
        limit: int = 100,
    ) -> List[schemas.Note]:
        q = db.query(self.model).filter(self.model.user_id == user_id)

        if orphaned:
            q = q.filter(self.model.notebook_id.is_(None))
        else:
            q = q.filter(self.model.notebook_id.isnot(None))
            
        if search:
            q = q.filter(
                or_(
                    func.lower(self.model.label.contains(func.lower(search))),
                    func.lower(self.model.body.contains(func.lower(search))),
                )
            )
            

        if sort == "rank":
            q = q.order_by(self.model.rank)

        notes = q.offset(skip).limit(limit).all()

        if order == "desc":
            notes.reverse()

        return notes

    def remove(self, db: Session, id: int, user_id: int) -> None:
        notebook = self.get_by_id_and_user_id(db, id=id, user_id=user_id)
        db.delete(notebook)
        db.commit()
        return

    def remove_all_by_notebook_id(self, db: Session, *, notebook_id: int) -> None:
        notes = db.query(self.model).filter(self.model.notebook_id == notebook_id).all()
        for note in notes:
            db.delete(note)
        db.commit()
        return

    def generate_rank(self, db: Session, notebook_id: Optional[int]) -> int:
        # determine custom order rank based on number of sibling notebooks
        return len(
            db.query(self.model)
            .filter(
                self.model.notebook_id == notebook_id,
            )
            .all()
        )

    def update_ranks(
        self, db: Session, *, update: schemas.NoteNewRank, user_id: int
    ) -> None:
        # get note
        note = self.get_by_id_and_user_id(db, id=update.id, user_id=user_id)
        # determine which notes to update
        start = update.rank if update.rank < note.rank else note.rank
        end = note.rank if update.rank < note.rank else update.rank
        # get notes
        notes: List[schemas.Note] = (
            db.query(self.model)
            .filter(
                self.model.rank.in_([i for i in range(start, end + 1)]),
                self.model.notebook_id == note.notebook_id,
                self.model.user_id == user_id,
            )
            .all()
        )
        # update rankings
        for n in notes:
            if update.rank > note.rank:
                n.rank -= 1
            else:
                n.rank += 1

            db.add(n)

        note.rank = update.rank
        db.add(note)

        db.commit()
        return


note = CRUDNote(models.Note)
