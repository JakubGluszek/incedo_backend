from fastapi import APIRouter

from . import account, notebooks, notes

router = APIRouter()
router.include_router(account.router, prefix="/account", tags=["Account"])
router.include_router(notes.router, prefix="/notes", tags=["Notes"])
router.include_router(notebooks.router, prefix="/notebooks", tags=["Notebooks"])
