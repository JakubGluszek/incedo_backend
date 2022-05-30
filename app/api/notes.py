from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from . import deps
from app import crud, schemas

router = APIRouter()


@router.post("", status_code=200, response_model=schemas.NoteOut)
async def create_note(
    note_in: schemas.NoteCreate,
    current_user: schemas.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    note = crud.note.create(db, note_in=note_in, user=current_user)
    return note
