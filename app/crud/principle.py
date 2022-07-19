from typing import List
from sqlalchemy.orm import Session

from app import models, schemas
from .base import CRUDBase


class CRUDPrinciple(
    CRUDBase[models.Principle, schemas.PrincipleCreate, schemas.PrincipleUpdate]
):
    def create(
        self, db: Session, *, principle_in: schemas.PrincipleCreate, user_id: int
    ) -> schemas.Principle:
        rank = self.generate_rank(db, user_id)
        principle = self.model(**principle_in.dict(), user_id=user_id, rank=rank)

        db.add(principle)
        db.commit()
        db.refresh(principle)

        return principle

    def generate_rank(self, db: Session, user_id: int) -> int:
        return len(db.query(self.model).filter(self.model.user_id == user_id).all())

    def remove(self, db: Session, *, id: int, user_id: int) -> None:
        principle = self.get_by_id_and_user_id(db, id=id, user_id=user_id)
        super().remove(db, principle.id)
        return

    def update_ranks(
        self, db: Session, *, update: schemas.PrincipleUpdateRanks, user_id: int
    ) -> None:
        principle = self.get_by_id_and_user_id(db, id=update.id, user_id=user_id)

        siblings: List[schemas.Principle] = (
            db.query(self.model).filter(self.model.user_id == user_id).all()
        )

        for s in siblings:
            if principle.rank > update.rank:
                if s.rank >= update.rank:
                    s.rank += 1
                    db.add(s)
            elif principle.rank < update.rank:
                if s.rank <= update.rank and s.rank > principle.rank:
                    s.rank -= 1
                    db.add(s)

        principle.rank = update.rank

        db.add(principle)
        db.commit()

        return


principle = CRUDPrinciple(models.Principle)
