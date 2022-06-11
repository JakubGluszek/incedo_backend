from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException

from .base import CRUDBase
from app import models, schemas


class CRUDNoteFolder(
    CRUDBase[models.NoteFolder, schemas.NoteFolderCreate, schemas.NoteFolderUpdate]
):
    class Errors:
        invalid_parent = {"loc": ["body", "parent_id"], "msg": "Invalid parent."}

    def create(
        self, db: Session, *, folder_in: schemas.NoteFolderCreate, user: schemas.User
    ) -> schemas.NoteFolder:
        if not folder_in.label:
            index = len(
                db.query(self.model)
                .filter(
                    self.model.parent_id == folder_in.parent_id,
                    self.model.user_id == user.id,
                )
                .all()
            )
            folder_in.label = f"Folder{index}"

        folder = self.model(**folder_in.dict(), user_id=user.id)

        db.add(folder)
        db.commit()
        db.refresh(folder)

        return folder

    def update(
        self,
        db: Session,
        *,
        id: int,
        update: schemas.NoteFolderUpdate,
        user: schemas.User,
    ) -> schemas.NoteFolder:
        # get valid folder
        folder = self.get(db, id)
        if not folder or folder.user_id != user.id:
            raise HTTPException(status_code=404)
        # validate parent
        if update.parent_id:
            parent = self.get(db, update.parent_id)
            if not parent or parent.user_id != user.id or parent.id == folder.id:
                raise HTTPException(
                    status_code=422, detail=[self.Errors.invalid_parent]
                )
        # update
        folder = super().update(db, db_obj=folder, obj_in=update)
        return folder

    def get_multi(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[schemas.NoteFolder]:
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


note_folder = CRUDNoteFolder(models.NoteFolder)
