from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class NoteFolderCreate(BaseModel):
    label: Optional[str] = Field(None, max_length=32)
    parent_id: Optional[int] = None


class NoteFolderUpdate(BaseModel):
    label: Optional[str] = Field(None, max_length=32)
    parent_id: Optional[int] = None


class NoteFolder(BaseModel):
    id: int
    label: str
    rank: int
    created_at: datetime
    edited_at: datetime
    parent_id: Optional[int] = None
    user_id: int


class NoteFolderOut(BaseModel):
    id: int
    label: str
    rank: int
    created_at: int
    edited_at: int
    parent_id: Optional[int] = None

    @validator("created_at", "edited_at", pre=True)
    def convert_to_timestamp(cls, v: datetime) -> int:
        return int(v.timestamp())

    class Config:
        orm_mode = True


class NoteFolderNewRank(BaseModel):
    id: int
    rank: int
    parent_id: Optional[int] = None
