from fastapi import BackgroundTasks, HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app import crud, schemas
from app.utils import mail


def create_account(
    db: Session, *, user_in: schemas.UserCreate, is_super: bool = False
) -> schemas.User:
    user = crud.user.create(db, user_in=user_in, is_super=is_super)
    crud.user_settings.create(db, user=user)
    return user


def create_and_send_token(db: Session, *, email: EmailStr, bg: BackgroundTasks) -> None:
    token = crud.token.create(db, email=email)
    bg.add_task(
        mail.send_token,
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
        user = create_account(db, user_in=user_in)

    crud.token.remove_by_email(db, token.email)

    return user


def sign_in_via_google(db: Session, *, code: dict) -> schemas.User:
    email = code["userinfo"]["email"]
    user = crud.user.get_by_email(db, email)

    if not user:
        user_in = schemas.UserCreate(email=email)
        create_account(db, user_in=user_in)

    return user


def delete_account(db: Session, *, user_id: int) -> None:
    user = crud.user.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404)

    crud.note.remove_all_by_user_id(db, user_id=user_id)
    crud.user_settings.remove_first_by_user_id(db, user_id=user_id)
    crud.user.remove(db, id=user_id)
    return
