from sqlalchemy.orm import Session

from .base import CRUDBase
from app import models, schemas
from app.core.security import get_password_hash


class CRUDUser(CRUDBase[models.User, schemas.UserCreate, schemas.UserUpdate]):
    def create(
        self, db: Session, *, user_in: schemas.UserCreate, is_super: bool = False
    ) -> models.User:
        db_user = models.User(
            **user_in.dict(exclude={"password", "password_repeat"}),
            password=get_password_hash(user_in.password),
            is_super=is_super
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


user = CRUDUser(models.User)
