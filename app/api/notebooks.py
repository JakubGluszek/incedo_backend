from typing import Any, List, Optional
from fastapi import APIRouter, Body, Depends, Query, Response
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
    notebook = crud.notebook.create(
        db, notebook_in=notebook_in, user_id=current_user.id
    )
    return notebook


@router.get("/{notebook_id}", response_model=schemas.NotebookWithNotes)
async def get_notebook(
    notebook_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    notebook = crud.notebook.get_by_id_and_user_id(
        db, id=notebook_id, user_id=current_user.id
    )
    return notebook


@router.get("", response_model=List[schemas.NotebookOut])
async def get_multi_notebooks(
    search: Optional[str] = None,
    sort: Optional[str] = None,
    order: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=0, le=100),
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    notebooks = crud.notebook.get_multi(
        db,
        user_id=current_user.id,
        search=search,
        sort=sort,
        order=order,
        skip=skip,
        limit=limit,
    )
    return notebooks


@router.put("/{notebook_id}", response_model=schemas.NotebookOut)
async def update_notebooks(
    notebook_id: int,
    update: schemas.NotebookUpdate,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    notebook = crud.notebook.update(
        db, id=notebook_id, update=update, user_id=current_user.id
    )
    return notebook


@router.delete("/{notebook_id}", status_code=204, response_class=Response)
async def remove_notebook(
    notebook_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    crud.notebook.remove_notebook_cascade(
        db, notebook_id=notebook_id, user_id=current_user.id
    )
    return


@router.delete("", status_code=204, response_class=Response)
async def remove_multi_notebooks(
    notebooks_ids: List[int] = Body(..., embed=True),
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    crud.notebook.remove_multi(db, objects_ids=notebooks_ids, user_id=current_user.id)
    return


@router.post("/ranks", response_class=Response)
async def update_notebooks_ranks(
    update: schemas.NotebookNewRank,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    crud.notebook.update_ranks(db, update=update, user_id=current_user.id)
    return
