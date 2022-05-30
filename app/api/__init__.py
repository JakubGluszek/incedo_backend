from fastapi import APIRouter

from . import account, notes, users

router = APIRouter()
router.include_router(account.router, prefix="/account", tags=["Account"])
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(notes.router, prefix="/notes", tags=["Notes"])
