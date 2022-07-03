from pydantic import EmailStr
from sqlalchemy.orm import Session

from app import crud, schemas


def create_user(db: Session) -> schemas.User:

    user_in = schemas.UserCreate(email="jacobgluszek03@gmail.com")
    user = crud.user.create(db, user_in=user_in)

    return user


def create_token(db: Session, *, email: EmailStr) -> str:
    return crud.token.create(db, email=email).token
