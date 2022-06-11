from typing import Optional
from pydantic import EmailStr
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException

from .base import CRUDBase
from app import models, schemas


class CRUDUser(CRUDBase[models.User, schemas.UserCreate, schemas.UserUpdate]):
    errors = {"email_taken": {"loc": ["body", "email"], "msg": "Email taken."}}

    def create(
        self,
        db: Session,
        *,
        user_in: schemas.UserCreate,
        is_super: bool = False,
    ) -> models.User:
        # validate
        if self.get_by_email(db, user_in.email):
            raise HTTPException(status_code=422, detail=[self.errors["email_taken"]])
        # create user
        user = models.User(
            **user_in.dict(exclude_none=True),
            is_super=is_super,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    def get_by_email(self, db: Session, email: EmailStr) -> Optional[schemas.User]:
        return (
            db.query(self.model)
            .filter(func.lower(self.model.email) == func.lower(email))
            .first()
        )

    def remove(self, db: Session, user: schemas.User) -> None:
        db.delete(user)
        db.commit()
        return


user = CRUDUser(models.User)
