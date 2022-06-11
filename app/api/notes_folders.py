from typing import Any, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps


router = APIRouter()


@router.post("")
async def create_notes_folder(
    folder_in: schemas.NoteFolderCreate,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    folder = crud.note_folder.create(db, folder_in=folder_in, user=current_user)
    return folder


@router.put("/{folder_id}")
async def update_notes_folder(
    folder_id: int,
    update: schemas.NoteFolderUpdate,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    folder = crud.note_folder.update(db, id=folder_id, update=update, user=current_user)
    return folder


@router.get("", response_model=List[schemas.NoteFolderOut], response_model_exclude={"notes"})
async def get_multi_notes_folders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=0, le=100),
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    folders = crud.note_folder.get_multi(
        db, user_id=current_user.id, skip=skip, limit=limit
    )
    return folders


@router.get("/{folder_id}", response_model=schemas.NoteFolderOut)
async def get_notes_folder(
    folder_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    folder = crud.note_folder.get_by_id_and_user(db, id=folder_id, user=current_user)
    return folder
