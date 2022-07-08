from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app import models, schemas

from .base import CRUDBase


class CRUDNoteFolder(
    CRUDBase[models.NoteFolder, schemas.NoteFolderCreate, schemas.NoteFolderUpdate]
):
    class Errors:
        parent_not_found = {"loc": ["body", "parent_id"], "msg": "Parent not found."}

    def create(
        self, db: Session, *, note_folder_in: schemas.NoteFolderCreate, user_id: int
    ) -> schemas.NoteFolder:
        # if given, validate parent note_folder
        if note_folder_in.parent_id:
            try:
                self.get_by_id_and_user_id(
                    db, id=note_folder_in.parent_id, user_id=user_id
                )
            except:
                raise HTTPException(
                    status_code=422, detail=[self.Errors.parent_not_found]
                )

        rank = self.generate_rank(
            db, user_id=user_id, parent_id=note_folder_in.parent_id
        )

        if not note_folder_in.label:
            if not note_folder_in.parent_id:
                note_folder_in.label = f"NoteFolder {rank + 1}"
            else:
                note_folder_in.label = f"Section {rank + 1}"

        note_folder = self.model(**note_folder_in.dict(), user_id=user_id, rank=rank)

        db.add(note_folder)
        db.commit()
        db.refresh(note_folder)

        return note_folder

    def update(
        self,
        db: Session,
        *,
        id: int,
        update: schemas.NoteFolderUpdate,
        user_id: int,
    ) -> schemas.NoteFolder:
        note_folder = self.get_by_id_and_user_id(db, id=id, user_id=user_id)

        if update.parent_id != note_folder.parent_id:
            if update.parent_id:
                try:
                    self.get_by_id_and_user_id(db, id=update.parent_id, user_id=user_id)
                except:
                    raise HTTPException(
                        status_code=422, detail=[self.Errors.parent_not_found]
                    )

            rank = self.generate_rank(db, user_id=user_id, parent_id=update.parent_id)
            note_folder.rank = rank

        note_folder.edited_at = datetime.utcnow()
        note_folder = super().update(
            db, db_obj=note_folder, obj_in=update.dict(exclude_unset=True)
        )
        return note_folder

    def remove_all_by_parent_id(self, db: Session, *, parent_id: int) -> None:
        sections = db.query(self.model).filter(self.model.parent_id == parent_id).all()
        for section in sections:
            db.delete(section)
        db.commit()
        return

    def get_multi(
        self,
        db: Session,
        *,
        user_id: int,
        search: Optional[str],
        sort: Optional[str],
        order: Optional[str],
        skip: int = 0,
        limit: Optional[int],
    ) -> List[schemas.NoteFolder]:
        q = db.query(self.model).filter(self.model.user_id == user_id)

        if search:
            q = q.outerjoin(
                models.Note, models.Note.note_folder_id == self.model.id
            ).filter(
                or_(
                    func.lower(self.model.label.contains(func.lower(search))),
                    func.lower(models.Note.label.contains(func.lower(search))),
                )
            )

        if sort == "rank":
            q = q.order_by(self.model.rank)

        q = q.offset(skip)

        if limit:
            q = q.limit(limit)

        note_folders = q.all()

        if order == "desc":
            note_folders.reverse()

        return note_folders

    def generate_rank(self, db: Session, parent_id: Optional[int], user_id: int) -> int:
        # determine custom order rank based on number of sibling note_folders
        return len(
            db.query(self.model)
            .filter(
                self.model.user_id == user_id,
                self.model.parent_id == parent_id,
            )
            .all()
        )

    def remove_note_folder_cascade(self, db: Session, *, id: int, user_id: int) -> None:
        note_folder = self.get_by_id_and_user_id(db, id=id, user_id=user_id)
        self.remove(db, id=note_folder.id)
        return


note_folder = CRUDNoteFolder(models.NoteFolder)
