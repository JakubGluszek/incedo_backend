from fastapi import BackgroundTasks, HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app import crud, schemas
from app.utils.mail import send_token_via_email


def send_token_via_email(db: Session, *, email: EmailStr, bg: BackgroundTasks) -> None:
    token = crud.token.create(db, email=email)
    bg.add_task(
        send_token_via_email,
        email_to=token.email,
        token=token.token,
    )
    return


def sign_in(db: Session, *, token_in: str) -> schemas.User:
    token = crud.token.get_by_token(db, token_in)
    if not token:
        raise HTTPException(status_code=404)

    user = crud.user.get_by_email(db, token.email)
    if not user:
        user_in = schemas.UserCreate(email=token.email)
        user = crud.user.create(db, user_in=user_in)

    crud.token.remove_by_email(db, token.email)

    return user


def sign_in_via_google(db: Session, *, code: dict) -> schemas.User:
    email = code["userinfo"]["email"]
    user = crud.user.get_by_email(db, email)
    if not user:
        user_in = schemas.UserCreate(email=email)
        user = crud.user.create(db, user_in=user_in)
    return user
