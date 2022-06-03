from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings


def init_db(db: Session) -> None:
    # Tables are created using Alembic migrations
    init_first_user(db)
    return


def init_first_user(db: Session) -> None:
    user_in = schemas.UserCreate(email=settings.FIRST_USER_EMAIL)
    crud.user.create(db, user_in=user_in, is_super=True)
    return