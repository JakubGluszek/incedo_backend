from fastapi import APIRouter, Depends

from app import schemas
from app.api import deps


router = APIRouter()


@router.get("", response_model=schemas.UserOut)
async def get_account(current_user: schemas.User = Depends(deps.get_current_user)):
    return current_user
