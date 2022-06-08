from fastapi import APIRouter

from . import auth, user, settings


router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(user.router, prefix="/user", tags=["User"])
router.include_router(settings.router, prefix="/settings", tags=["Settings"])
