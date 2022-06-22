from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

from .base import CRUDBase
from app import models, schemas


class CRUDNotebook(
    CRUDBase[models.Notebook, schemas.NotebookCreate, schemas.NotebookUpdate]
):
    class Errors:
        not_found_422 = {"loc": ["body", "id"], "msg": "Notebook not found."}

    def create(
        self, db: Session, *, notebook_in: schemas.NotebookCreate, user: schemas.User
    ) -> schemas.Notebook:
        last = self.get_last_rank(db, user=user)
        if last:
            rank = last.rank + 1
        else:
            rank = 0
        if not notebook_in.label:
            notebook_in.label = f"Notebook {rank + 1}"

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

    # update / replace ranks between notebooks
    def update_rank(
        self, db: Session, *, update: schemas.NotebookUpdateRank, user: schemas.User
    ) -> List[schemas.Notebook]:
        notebook = self.get_by_id_and_user(db, id=update.id, user=user)
        if not notebook:
            raise HTTPException(
                status_code=422,
                detail=[self.Errors.not_found_422],
            )
        other_notebook = self.get_by_rank_and_user(db, rank=update.rank, user=user)
        if other_notebook:
            other_notebook.rank = notebook.rank
            db.add(other_notebook)

        notebook.rank = update.rank
        db.add(notebook)
        db.commit()

        return [notebook, other_notebook]

    def get_by_rank_and_user(
        self, db: Session, *, rank: int, user: schemas.User
    ) -> Optional[schemas.Notebook]:
        return (
            db.query(self.model)
            .filter(self.model.rank == rank, self.model.user_id == user.id)
            .first()
        )

    def get_last_rank(
        self, db: Session, *, user: schemas.User
    ) -> Optional[schemas.Notebook]:
        notebooks = (
            db.query(self.model)
            .filter(self.model.user_id == user.id)
            .order_by(self.model.rank)
            .all()
        )
        if len(notebooks) > 0:
            return notebooks[-1]
        return None


notebook = CRUDNotebook(models.Notebook)
