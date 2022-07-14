from fastapi import APIRouter

from . import notes, note_folders

router = APIRouter()
#router.include_router(
#    note_folders.router, prefix="/notes/folders", tags=["Note Folders"]
#)
router.include_router(notes.router, prefix="/notes", tags=["Notes"])
