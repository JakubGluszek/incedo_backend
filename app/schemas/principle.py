from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator


class PrincipleCreate(BaseModel):
    body: str


class PrincipleUpdate(BaseModel):
    body: Optional[str] = None


class Principle(BaseModel):
    id: int
    body: str
    rank: int
    user_id: int
    created_at: datetime


class PrincipleOut(BaseModel):
    id: int
    body: str
    rank: int
    created_at: int

    @validator("created_at", pre=True)
    def convert_to_timestamp(cls, v: datetime) -> int:
        return int(v.timestamp())

    class Config:
        orm_mode = True


class PrincipleUpdateRanks(BaseModel):
    id: int
    rank: int
