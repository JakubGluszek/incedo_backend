from fastapi import APIRouter, Depends

from . import deps
from app import schemas


router = APIRouter()


@router.get("/me", response_model=schemas.User, response_model_exclude={"password"})
async def read_users_me(current_user: schemas.User = Depends(deps.get_current_user)):
    return current_user
