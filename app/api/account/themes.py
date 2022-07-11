from typing import Any
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.post("")
async def create_theme(
    theme_in: schemas.ThemeCreate,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    theme = crud.theme.create(db, theme_in, user_id=current_user.id)
    return theme


@router.get("")
async def get_multi_themes(
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    themes = crud.theme.get_multi(db, user_id=current_user.id)
    return themes


@router.get("/{id}")
async def get_theme(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    theme = crud.theme.get_by_id_and_user_id(db, id=id, user_id=current_user.id)
    return theme


@router.put("/{id}")
async def update_theme(
    id: int,
    update: schemas.ThemeUpdate,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    theme = crud.theme.update(db, id=id, update=update, user_id=current_user.id)
    return theme


@router.delete("/{id}", status_code=204, response_class=Response)
async def remove_theme(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    crud.theme.remove(db, id=id, user_id=current_user.id)
    return
