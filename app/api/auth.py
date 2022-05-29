from typing import Any
from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import deps
from app import crud, schemas


router = APIRouter()


@router.post("/register", status_code=201, response_class=Response)
async def register(
    user_in: schemas.UserCreate, db: Session = Depends(deps.get_db)
) -> Any:
    crud.user.create(db, user_in=user_in)
    return


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    return crud.user.login(db, form_data=form_data)
