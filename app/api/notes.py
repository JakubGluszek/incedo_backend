from typing import Any, List, Optional

from fastapi import APIRouter, Body, Depends, Query, Response
from sqlalchemy.orm import Session

from app import crud, schemas

from . import deps

router = APIRouter()


@router.post("", status_code=200, response_model=schemas.NoteOut)
async def create_note(
    note_in: schemas.NoteCreate,
    current_user: schemas.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    note = crud.note.create(db, note_in=note_in, user_id=current_user.id)
    return note


@router.get("/{note_id}", response_model=schemas.NoteOut)
async def get_note(
    note_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    note = crud.note.get_by_id_and_user_id(db, id=note_id, user_id=current_user.id)
    return note


@router.get("", response_model=List[schemas.NoteOut])
async def get_multi_notes(
    search: Optional[str] = None,
    sort: Optional[str] = None,
    order: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=0, le=100),
    orphaned: bool = Query(
        False,
        description="Get multi notes with notebook_id == null. These notes are scheduled for deletion.",
    ),
    current_user: schemas.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    return crud.note.get_multi(
        db,
        user_id=current_user.id,
        search=search,
        sort=sort,
        order=order,
        orphaned=orphaned,
        skip=skip,
        limit=limit,
    )


@router.put("/{id}", response_model=schemas.NoteOut)
async def update_note(
    id: int,
    update: schemas.NoteUpdate,
    current_user: schemas.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    note = crud.note.update(db, id=id, update=update, user_id=current_user.id)
    return note


@router.delete("/{id}", status_code=204, response_class=Response)
async def remove_note(
    id: int,
    current_user: schemas.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    crud.note.remove(db, id=id, user_id=current_user.id)
    return


@router.delete("", status_code=204, response_class=Response)
async def remove_multi_notes(
    notes_ids: List[int] = Body(..., embed=True),
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    crud.note.remove_multi(db, objects_ids=notes_ids, user_id=current_user.id)
    return


@router.post("/ranks", response_class=Response)
async def update_notes_ranks(
    update: schemas.NoteNewRank,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    crud.note.update_ranks(db, update=update, user_id=current_user.id)
    return
