from typing import Any, List
from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps


router = APIRouter()


@router.post("", response_model=schemas.PrincipleOut)
async def create_principle(
    principle_in: schemas.PrincipleCreate,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    return crud.principle.create(db, principle_in=principle_in, user_id=current_user.id)


@router.get("/{id}", response_model=schemas.PrincipleOut)
async def get_principle(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    return crud.principle.get_by_id_and_user_id(db, id=id, user_id=current_user.id)


@router.get("", response_model=List[schemas.PrincipleOut])
async def get_multi_principles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=0, le=100),
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    return crud.principle.get_multi(db, user_id=current_user.id, skip=skip, limit=limit)


@router.delete("/{id}", status_code=204, response_class=Response)
async def remove_principle(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    return crud.principle.remove(db, id=id, user_id=current_user.id)


@router.post("/ranks", status_code=200, response_class=Response)
async def update_principles_ranks(
    update: schemas.PrincipleUpdateRanks,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    return crud.principle.update_ranks(db, update=update, user_id=current_user.id)
