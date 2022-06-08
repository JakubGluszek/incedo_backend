from typing import Any, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from . import deps
from app import services, schemas, crud


router = APIRouter()


@router.post("", response_model=schemas.DailyNoteOut)
async def create_daily_note(
    note_in: schemas.DailyNoteCreate,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    note = services.create_daily_note(db, note_in=note_in, user=current_user)
    return note


@router.get("", response_model=List[schemas.DailyNoteOut])
async def get_multi_daily_notes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=0, le=100),
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    notes = crud.daily_note.get_multi(db, user=current_user, skip=skip, limit=limit)
    return notes


@router.get("/today", response_model=schemas.DailyNoteOut)
async def get_daily_note(
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    note = crud.daily_note.get_todays(db, user=current_user)
    return note


@router.put("/today", response_model=schemas.DailyNoteOut)
async def update_daily_note(
    update: schemas.DailyNoteUpdate,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    note = services.update_daily_note(db, update=update, user=current_user)
    return note
