from typing import Generator
from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db.session import SessionLocal


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
) -> schemas.User:
    Authorize.jwt_required()

    id = Authorize.get_jwt_subject()
    user = crud.user.get(db, id)

    if not user:
        raise HTTPException(status_code=401)
    return user
