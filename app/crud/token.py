from typing import Optional

from pydantic import EmailStr
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models

from .base import CRUDBase


class CRUDToken(CRUDBase[models.Token, None, None]):
    def create(self, db: Session, *, email: EmailStr) -> models.Token:
        token = self.get_by_email(db, email)

        if token:
            if not token.expired:
                return token
            else:
                db.delete(token)
                db.commit()

        token = self.model(email=email)

        db.add(token)
        db.commit()
        db.refresh(token)

        return token

    def get_by_email(self, db: Session, email: EmailStr) -> Optional[models.Token]:
        return (
            db.query(self.model)
            .filter(func.lower(self.model.email) == func.lower(email))
            .first()
        )

    def get_by_token(self, db: Session, token: str) -> Optional[models.Token]:
        return db.query(self.model).filter(self.model.token == token).first()

    def remove_by_email(self, db: Session, email: EmailStr) -> None:
        token = self.get_by_email(db, email)
        if not token:
            return
        db.delete(token)
        db.commit()
        return


token = CRUDToken(models.Token)
