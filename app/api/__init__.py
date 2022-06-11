from fastapi import APIRouter

from . import account, notes, daily_notes, notes_folders

router = APIRouter()
router.include_router(account.router, prefix="/account", tags=["Account"])
router.include_router(notes.router, prefix="/notes", tags=["Notes"])
router.include_router(notes_folders.router, prefix="/notes_folders", tags=["Notes", "Folders"])
router.include_router(daily_notes.router, prefix="/daily_notes", tags=["Daily Notes"])
