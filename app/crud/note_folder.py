from sqlalchemy.orm import Session
from fastapi import HTTPException

from .base import CRUDBase
from app import models, schemas


class CRUDNoteFolder(
    CRUDBase[models.NoteFolder, schemas.NoteFolderCreate, schemas.NoteFolderUpdate]
):
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


note_folder = CRUDNoteFolder(models.NoteFolder)
