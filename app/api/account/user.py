from typing import Any
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app import schemas, services
from app.api import deps


router = APIRouter()


@router.get("", response_model=schemas.UserOut)
async def get_current_user(
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    return current_user


@router.delete("", status_code=204, response_class=Response)
async def remove_current_user(
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    services.account.delete_account(db, user_id=current_user.id)
    return
