from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from . import deps
from app import crud, schemas


router = APIRouter()


@router.get("", response_model=List[schemas.UserOut])
async def get_users(skip: int = 0, db: Session = Depends(deps.get_db)) -> Any:
    return crud.user.get_multi(db, skip=skip)
