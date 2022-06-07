from fastapi import APIRouter

from . import account, users, notes, daily_notes

router = APIRouter()
router.include_router(account.router, prefix="/account", tags=["Account"])
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(notes.router, prefix="/notes", tags=["Notes"])
router.include_router(daily_notes.router, prefix="/daily_notes", tags=["Daily Notes"])
