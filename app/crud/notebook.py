from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy import func, or_
from sqlalchemy.orm import Session, Query 

from .base import CRUDBase
from app import models, schemas


class CRUDNotebook(
    CRUDBase[models.Notebook, schemas.NotebookCreate, schemas.NotebookUpdate]
):
    class Errors:
        parent_not_found = {"loc": ["body", "parent_id"], "msg": "Parent not found."}

    def create(
        self, db: Session, *, notebook_in: schemas.NotebookCreate, user_id: int
    ) -> schemas.Notebook:
        # if given, validate parent notebook
        if notebook_in.parent_id:
            try:
                self.get_by_id_and_user_id(
                    db, id=notebook_in.parent_id, user_id=user_id
                )
            except:
                raise HTTPException(
                    status_code=422, detail=[self.Errors.parent_not_found]
                )

        rank = self.generate_rank(db, user_id=user_id, parent_id=notebook_in.parent_id)

        if not notebook_in.label:
            if not notebook_in.parent_id:
                notebook_in.label = f"Notebook {rank + 1}"
            else:
                notebook_in.label = f"Section {rank + 1}"

        notebook = self.model(**notebook_in.dict(), user_id=user_id, rank=rank)

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
        user_id: int,
    ) -> schemas.Notebook:
        notebook = self.get_by_id_and_user_id(db, id=id, user_id=user_id)

        if update.parent_id != notebook.parent_id:
            if update.parent_id:
                try:
                    self.get_by_id_and_user_id(db, id=update.parent_id, user_id=user_id)
                except:
                    raise HTTPException(
                        status_code=422, detail=[self.Errors.parent_not_found]
                    )

            rank = self.generate_rank(db, user_id=user_id, parent_id=update.parent_id)
            notebook.rank = rank

        notebook.edited_at = datetime.utcnow()
        notebook = super().update(
            db, db_obj=notebook, obj_in=update.dict(exclude_unset=True)
        )
        return notebook

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
        limit: int = 100,
    ) -> List[schemas.Notebook]:
        q = db.query(self.model).filter(self.model.user_id == user_id)

        if search:
            q = q.outerjoin(
                models.Note, models.Note.notebook_id == self.model.id
            ).filter(
                or_(
                    func.lower(self.model.label.contains(func.lower(search))),
                    func.lower(models.Note.label.contains(func.lower(search))),
                )
            )

        if sort == "rank":
            q = q.order_by(self.model.rank)

        notebooks = q.offset(skip).limit(limit).all()

        if order == "desc":
            notebooks.reverse()

        return notebooks

    def generate_rank(self, db: Session, parent_id: Optional[int], user_id: int) -> int:
        # determine custom order rank based on number of sibling notebooks
        return len(
            db.query(self.model)
            .filter(
                self.model.user_id == user_id,
                self.model.parent_id == parent_id,
            )
            .all()
        )

    def remove_notebook_cascade(
        self, db: Session, *, notebook_id: int, user_id: int
    ) -> None:
        notebook = self.get_by_id_and_user_id(db, id=notebook_id, user_id=user_id)
        self.remove(db, id=notebook.id)
        return

    def update_ranks(
        self, db: Session, *, update: schemas.NotebookNewRank, user_id: int
    ) -> None:
        # get notebook
        notebook = self.get_by_id_and_user_id(db, id=update.id, user_id=user_id)
        # get notebooks
        start = update.rank if update.rank < notebook.rank else notebook.rank
        end = notebook.rank if update.rank < notebook.rank else update.rank
        notebooks: List[schemas.Notebook] = (
            db.query(self.model)
            .filter(
                self.model.rank.in_([i for i in range(start, end + 1)]),
                self.model.parent_id == notebook.parent_id,
                self.model.user_id == user_id,
            )
            .all()
        )
        # update rankings
        for n in notebooks:
            if update.rank > notebook.rank:
                n.rank -= 1
            else:
                n.rank += 1

            db.add(n)

        notebook.rank = update.rank
        db.add(notebook)

        db.commit()
        return


notebook = CRUDNotebook(models.Notebook)
