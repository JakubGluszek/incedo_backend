from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


class NotebookCreate(BaseModel):
    label: Optional[str] = Field(None, max_length=32)
    parent_id: Optional[int] = None


class NotebookUpdate(BaseModel):
    label: Optional[str] = Field(None, max_length=32)
    parent_id: Optional[int] = None


class Notebook(BaseModel):
    id: int
    label: str
    rank: int
    created_at: datetime
    edited_at: datetime
    parent_id: Optional[int] = None
    user_id: int


class NotebookOut(BaseModel):
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


class NotebookNewRank(BaseModel):
    id: int
    rank: int
