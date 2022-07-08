from typing import Any, List, Optional

from fastapi import APIRouter, Body, Depends, Query, Response
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps


router = APIRouter()


class NoteFolderWithNotes(schemas.NoteFolderOut):
    notes: List[schemas.NoteOut]
    sections: List[schemas.NoteFolderOut]


@router.post("", response_model=schemas.NoteFolderOut)
async def create_note_folders(
    note_folder_in: schemas.NoteFolderCreate,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    note_folder = crud.note_folder.create(
        db, note_folder_in=note_folder_in, user_id=current_user.id
    )
    return note_folder


@router.get("/{id}", response_model=NoteFolderWithNotes)
async def get_note_folder(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    note_folder = crud.note_folder.get_by_id_and_user_id(
        db, id=id, user_id=current_user.id
    )
    return note_folder


@router.get("", response_model=List[schemas.NoteFolderOut])
async def get_multi_note_folders(
    search: Optional[str] = None,
    sort: Optional[str] = None,
    order: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(None, ge=0),
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    note_folders = crud.note_folder.get_multi(
        db,
        user_id=current_user.id,
        search=search,
        sort=sort,
        order=order,
        skip=skip,
        limit=limit,
    )
    return note_folders


@router.put("/{id}", response_model=schemas.NoteFolderOut)
async def update_note_folders(
    id: int,
    update: schemas.NoteFolderUpdate,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    note_folder = crud.note_folder.update(
        db, id=id, update=update, user_id=current_user.id
    )
    return note_folder


@router.delete("/{id}", status_code=204, response_class=Response)
async def remove_note_folder(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    crud.note_folder.remove_note_folder_cascade(db, id=id, user_id=current_user.id)
    return


@router.delete("", status_code=204, response_class=Response)
async def remove_multi_note_folders(
    note_folders_ids: List[int] = Body(..., embed=True),
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    crud.note_folder.remove_multi(
        db, objects_ids=note_folders_ids, user_id=current_user.id
    )
    return
