from fastapi import APIRouter
from fastapi_jwt_auth import AuthJWT

from . import account, notebooks, notes
from app.core.config import JWTSettings, settings

router = APIRouter()
router.include_router(account.router, prefix="/account", tags=["Account"])
router.include_router(notes.router, prefix="/notes", tags=["Notes"])
router.include_router(notebooks.router, prefix="/notebooks", tags=["Notebooks"])


@AuthJWT.load_config
def get_config():
    jwt_settings = JWTSettings()
    if settings.DEVELOPMENT:
        del jwt_settings.authjwt_cookie_domain
    return jwt_settings
