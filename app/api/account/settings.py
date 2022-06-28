from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps


router = APIRouter()


@router.get("", response_model=schemas.UserSettingsOut)
async def get_user_settings(
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    return crud.user_settings.get_by_user_id(db, user_id=current_user.id)


@router.put("", response_model=schemas.UserSettingsOut)
async def update_user_settings(
    update: schemas.UserSettingsUpdate,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    settings = crud.user_settings.update(db, update=update, user_id=current_user.id)
    return settings
