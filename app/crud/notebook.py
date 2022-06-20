from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException

from .base import CRUDBase
from app import models, schemas


class CRUDNotebook(
    CRUDBase[models.Notebook, schemas.NotebookCreate, schemas.NotebookUpdate]
):
    def create(
        self, db: Session, *, notebook_in: schemas.NotebookCreate, user: schemas.User
    ) -> schemas.Notebook:
        rank = len(
            db.query(self.model)
            .filter(
                self.model.user_id == user.id,
            )
            .all()
        )
        if not notebook_in.label:
            notebook_in.label = f"Notebook {rank}"

        notebook = self.model(**notebook_in.dict(), user_id=user.id, rank=rank)

        db.add(notebook)
        db.commit()
        db.refresh(notebook)

        return notebook

    def update(
        self,
        db: Session,
        *,
        id: int,
        update: schemas.NotebookUpdate,
        user: schemas.User,
    ) -> schemas.Notebook:
        # get valid notebook
        notebook = self.get(db, id)
        if not notebook or notebook.user_id != user.id:
            raise HTTPException(status_code=404)
        # update
        notebook = super().update(db, db_obj=notebook, obj_in=update)
        return notebook

    def get_multi(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[schemas.Notebook]:
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def remove(self, db: Session, *, id: int, user: schemas.User) -> None:
        notebook = self.get_by_id_and_user(db, id=id, user=user)
        super().remove(db, id=notebook.id)
        return


notebook = CRUDNotebook(models.Notebook)
