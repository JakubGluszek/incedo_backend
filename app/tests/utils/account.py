import json
from typing import Dict

from fastapi.testclient import TestClient
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app import crud, schemas, services
from app.core.config import settings


def create_account(db: Session) -> schemas.User:

    user_in = schemas.UserCreate(email="jacobgluszek03@gmail.com")
    user = services.account.create_account(db, user_in=user_in)

    return user


def create_token(db: Session, *, email: EmailStr) -> str:
    return crud.token.create(db, email=email).token


def get_current_test_user_headers(client: TestClient, db_session: Session) -> Dict:
    user = create_account(db_session)
    token = create_token(db_session, email=user.email)

    data = {"token": token}

    r = client.post(f"{settings.HOST}/account/auth/signin", data=json.dumps(data))

    payload: schemas.Tokens = r.json()

    return {"Authorization": f"Bearer {payload['access_token']}"}
