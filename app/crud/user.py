from datetime import timedelta
from typing import Optional
from pydantic import EmailStr
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from .base import CRUDBase
from app import models, schemas
from app.core import security
from app.core.config import settings


class CRUDUser(CRUDBase[models.User, schemas.UserCreate, schemas.UserUpdate]):
    errors = {"email_taken": {"loc": ["body", "email"], "msg": "Email taken."}}

    def create(
        self,
        db: Session,
        *,
        user_in: schemas.UserCreate,
        is_super: bool = False,
        email_verified: bool = False
    ) -> models.User:
        # validate
        if self.get_by_email(db, user_in.email):
            raise HTTPException(status_code=422, detail=[self.errors["email_taken"]])

        # create user
        user = models.User(
            **user_in.dict(exclude={"password", "password_repeat"}),
            password=security.get_password_hash(user_in.password),
            is_super=is_super,
            email_verified=email_verified
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_by_email(self, db: Session, email: EmailStr) -> Optional[models.User]:
        return (
            db.query(self.model)
            .filter(func.lower(self.model.email) == func.lower(email))
            .first()
        )

    def authenticate(
        self, db: Session, *, email: EmailStr, password: str
    ) -> Optional[models.User]:
        user = self.get_by_email(db, email)
        if not user:
            return None
        if not security.verify_password(password, user.password):
            return None
        return user

    def login(
        self, db: Session, *, form_data: OAuth2PasswordRequestForm
    ) -> schemas.Token:
        user = self.authenticate(
            db, email=form_data.username, password=form_data.password
        )
        if not user:
            raise HTTPException(status_code=422)
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = schemas.Token(
            access_token=security.create_access_token(
                data={"sub": str(user.id)}, expires_delta=access_token_expires
            ),
            token_type="bearer",
        )
        return token


user = CRUDUser(models.User)
