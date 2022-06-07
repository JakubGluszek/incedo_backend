from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from . import deps
from app import services, schemas


router = APIRouter()


@router.post("")
async def create_daily_note(
    note_in: schemas.DailyNoteCreate,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    note = services.create_daily_note(db, note_in=note_in, user=current_user)
    return note
