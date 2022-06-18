from typing import Any, List
from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from . import deps
from app import crud, schemas

router = APIRouter()


@router.post("", status_code=200, response_model=schemas.NoteOut)
async def create_note(
    note_in: schemas.NoteCreate,
    current_user: schemas.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    note = crud.note.create(db, note_in=note_in, user=current_user)
    return note


@router.put("/{id}", response_model=schemas.NoteOut)
async def update_note(
    id: int,
    update: schemas.NoteUpdate,
    current_user: schemas.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    note = crud.note.update(db, id=id, update=update, user=current_user)
    return note


@router.delete("/{id}", status_code=204, response_class=Response)
async def remove_note(
    id: int,
    current_user: schemas.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    crud.note.remove(db, id=id, user=current_user)
    return


@router.get("/{note_id}", response_model=schemas.NoteOut)
async def get_note(
    note_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    note = crud.note.get_by_id_and_user(db, id=note_id, user=current_user)
    return note


@router.get("", response_model=List[schemas.NoteOut])
async def get_multi_notes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=0, le=100),
    current_user: schemas.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    notes = crud.note.get_multi(db, user_id=current_user.id, skip=skip, limit=limit)
    return notes
