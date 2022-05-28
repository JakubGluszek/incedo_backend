from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings


def init_db(db: Session) -> None:
    # Tables are created using Alembic migrations
    init_first_user(db)
    return


def init_first_user(db: Session) -> None:
    user_in = schemas.UserCreate(
        username=settings.FIRST_USER_USERNAME,
        email=settings.FIRST_USER_EMAIL,
        password=settings.FIRST_USER_PASSWORD,
        password_repeat=settings.FIRST_USER_PASSWORD,
    )
    crud.user.create(db, user_in=user_in, is_super=True, email_verified=True)
    return
