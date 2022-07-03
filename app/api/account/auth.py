from typing import Any

from fastapi import APIRouter, BackgroundTasks, Body, Depends, Request
from fastapi.responses import JSONResponse, RedirectResponse, Response
from fastapi_jwt_auth import AuthJWT
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app import schemas, services
from app.api import deps
from app.core.config import settings
from app.utils.oauth import oauth

router = APIRouter()


@router.post("/token", response_class=Response)
async def get_token_via_email(
    bg: BackgroundTasks,
    email: EmailStr = Body(..., embed=True),
    db: Session = Depends(deps.get_db),
) -> Any:
    services.account.create_and_send_token(db, email=email, bg=bg)
    return


@router.post("/signin", response_model=schemas.UserOut)
async def sign_in(
    response: JSONResponse,
    token: str = Body(..., embed=True),
    db: Session = Depends(deps.get_db),
    Authorize: AuthJWT = Depends(),
) -> Any:
    user = services.account.sign_in(db, token_in=token)

    access_token = Authorize.create_access_token(subject=user.id)
    refresh_token = Authorize.create_refresh_token(subject=user.id)

    Authorize.set_access_cookies(access_token, response)
    Authorize.set_refresh_cookies(refresh_token, response)

    return user


@router.get("/signin/google")
async def sign_in_via_google(request: Request) -> Any:
    redirect_uri = request.url_for("sign_in_via_google_callback").replace(
        "http", "https"
    )
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/signin/google/callback", include_in_schema=False)
async def sign_in_via_google_callback(
    request: Request, db: Session = Depends(deps.get_db), Authorize: AuthJWT = Depends()
) -> Any:
    code = await oauth.google.authorize_access_token(request)
    user = services.account.sign_in_via_google(db, code=code)

    response = RedirectResponse(settings.FRONTEND_HOST)

    access_token = Authorize.create_access_token(subject=user.id)
    refresh_token = Authorize.create_refresh_token(subject=user.id)
    Authorize.set_access_cookies(access_token, response)
    Authorize.set_refresh_cookies(refresh_token, response)

    return response


@router.post("/refresh")
async def refresh_token(Authorize: AuthJWT = Depends()) -> Any:
    Authorize.jwt_refresh_token_required()

    user_id = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=user_id)

    response = Response()

    Authorize.set_access_cookies(new_access_token, response)

    return response
