import json

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.tests.utils.account import create_token, create_account


def test_get_token_via_email(client: TestClient, db_session: Session) -> None:
    data = {"email": "jacobgluszek03@gmail.com"}
    r = client.post(f"{settings.HOST}/account/auth/token", data=json.dumps(data))

    assert r.status_code == 200

    token = crud.token.get_by_email(db_session, email=data["email"])

    assert token

    return


def test_signin(client: TestClient, db_session: Session) -> None:
    user = create_account(db_session)
    token = create_token(db_session, email=user.email)

    data = {"token": token}

    r = client.post(f"{settings.HOST}/account/auth/signin", data=json.dumps(data))

    assert r.status_code == 200

    payload = r.json()

    assert payload["access_token"]
    assert payload["refresh_token"]

    return
