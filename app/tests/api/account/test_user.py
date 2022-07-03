import json

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.account import get_current_test_user_headers


def test_get_current_user(client: TestClient, db_session: Session) -> None:
    headers = get_current_test_user_headers(client, db_session)
    r = client.get(f"{settings.HOST}/account/user", headers=headers)

    payload = r.json()

    assert r.status_code == 200
    assert payload["email"] == "jacobgluszek03@gmail.com"

    return


def test_delete_current_user(client: TestClient, db_session: Session) -> None:
    headers = get_current_test_user_headers(client, db_session)
    print(headers)
    r = client.delete(f"{settings.HOST}/account/user", headers=headers)

    assert r.status_code == 204

    return
