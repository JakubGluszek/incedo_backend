import json

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.account import create_token, create_user


def test_get_token_via_email(client: TestClient) -> None:
    data = {"email": "jacobgluszek03@gmail.com"}
    r = client.post(f"{settings.HOST}/account/auth/token", data=json.dumps(data))

    assert r.status_code == 200
    return


def test_signin(client: TestClient, db_session: Session) -> None:
    user = create_user(db_session)
    token = create_token(db_session, email=user.email)

    data = {"token": token}

    r = client.post(f"{settings.HOST}/account/auth/signin", data=json.dumps(data))

    assert r.status_code == 200

    payload = r.json()

    assert payload["email"] == user.email

    return
