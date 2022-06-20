from typing import Any, List
from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps


router = APIRouter()


@router.post("", response_model=schemas.NotebookOut)
async def create_notebooks(
    notebook_in: schemas.NotebookCreate,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    notebook = crud.notebook.create(db, notebook_in=notebook_in, user=current_user)
    return notebook


@router.put("/{notebook_id}")
async def update_notebooks(
    notebook_id: int,
    update: schemas.NotebookUpdate,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    notebook = crud.notebook.update(
        db, id=notebook_id, update=update, user=current_user
    )
    return notebook


@router.delete("/{notebook_id}", status_code=204, response_class=Response)
async def remove_notebooks(
    notebook_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    crud.notebook.remove(db, id=notebook_id, user=current_user)
    return


@router.get("", response_model=List[schemas.NotebookOut])
async def get_multi_notebooks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=0, le=100),
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    notebooks = crud.notebook.get_multi(
        db, user_id=current_user.id, skip=skip, limit=limit
    )
    return notebooks


@router.get("/{notebook_id}", response_model=schemas.NotebookOut)
async def get_notebook(
    notebook_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    notebook = crud.notebook.get_by_id_and_user(db, id=notebook_id, user=current_user)
    return notebook
