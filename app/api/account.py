from typing import Any
from fastapi import APIRouter, BackgroundTasks, Body, Depends, Request
from fastapi.responses import RedirectResponse, Response, JSONResponse
from pydantic import EmailStr
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from fastapi_jwt_auth import AuthJWT

from . import deps
from app import schemas
from app.services import auth
from app.core.config import JWTSettings, settings


config = Config(".env")
oauth = OAuth(config)
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email"},
)


@AuthJWT.load_config
def get_config():
    return JWTSettings()


router = APIRouter()


@router.get("", response_model=schemas.User)
async def get_account(current_user: schemas.User = Depends(deps.get_current_user)):
    return current_user


@router.post("/token", response_class=Response)
async def get_token_via_email(
    bg: BackgroundTasks,
    email: EmailStr = Body(..., embed=True),
    db: Session = Depends(deps.get_db),
) -> Any:
    auth.send_token_via_email(db, email=email, bg=bg)
    return


@router.post("/signin", response_model=schemas.User)
async def sign_in(
    response: JSONResponse,
    token: str = Body(..., embed=True),
    db: Session = Depends(deps.get_db),
    Authorize: AuthJWT = Depends(),
) -> Any:
    user = auth.sign_in(db, token_in=token)

    access_token = Authorize.create_access_token(subject=user.id)
    refresh_token = Authorize.create_refresh_token(subject=user.id)

    Authorize.set_access_cookies(access_token, response)
    Authorize.set_refresh_cookies(refresh_token, response)

    return user


@router.get("/signin/google")
async def sign_in_via_google(request: Request) -> Any:
    # redirect_uri = request.url_for("sign_in_via_google_callback")
    redirect_uri = "http://127.0.0.1:8000/account/signin/google/callback"  # dev mode
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/signin/google/callback", include_in_schema=False)
async def sign_in_via_google_callback(
    request: Request, db: Session = Depends(deps.get_db), Authorize: AuthJWT = Depends()
) -> Any:
    code = await oauth.google.authorize_access_token(request)
    user = auth.login_via_google(db, code=code)

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
