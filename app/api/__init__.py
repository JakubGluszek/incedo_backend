from fastapi import APIRouter
from fastapi_jwt_auth import AuthJWT

from app.core.config import JWTSettings, settings

from . import account, notes

router = APIRouter()
router.include_router(account.router, prefix="/account")
router.include_router(notes.router)


@AuthJWT.load_config
def get_config():
    jwt_settings = JWTSettings()
    if settings.DEVELOPMENT:
        del jwt_settings.authjwt_cookie_domain
    return jwt_settings
