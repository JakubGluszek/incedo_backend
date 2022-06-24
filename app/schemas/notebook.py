from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, validator


class NotebookCreate(BaseModel):
    label: Optional[str] = Field(None, max_length=32)
    about: Optional[str] = Field(None, max_length=256)


class NotebookUpdate(BaseModel):
    label: Optional[str] = Field(None, max_length=32)
    about: Optional[str] = Field(None, max_length=256)


class Notebook(BaseModel):
    id: int
    label: str
    about: Optional[str]
    rank: int
    created_at: datetime
    edited_at: datetime
    user_id: int


class NotebookOut(BaseModel):
    id: int
    label: str
    rank: int
    about: Optional[str] = None
    created_at: int
    edited_at: int

    @validator("created_at", "edited_at", pre=True)
    def convert_to_timestamp(cls, v: datetime) -> int:
        return int(v.timestamp())

    notes: List[NoteOut]
    class Config:
        orm_mode = True


class NotebookUpdateRank(BaseModel):
    id: int
    rank: int


from app.schemas.note import NoteOut

NotebookOut.update_forward_refs()
