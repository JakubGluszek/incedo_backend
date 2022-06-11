from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field


class NoteFolderCreate(BaseModel):
    label: Optional[str] = Field(None, max_length=32)
    parent_id: Optional[int] = None


class NoteFolderUpdate(BaseModel):
    label: Optional[str] = Field(None, max_length=32)
    parent_id: Optional[int] = None


class NoteFolder(BaseModel):
    id: int
    label: str
    parent_id: Optional[int]
    user_id: int


class NoteFolderOut(BaseModel):
    id: int
    label: str
    parent_id: Optional[int]
    notes: List[NoteOut]

    class Config:
        orm_mode = True


from app.schemas import NoteOut

NoteFolderOut.update_forward_refs()
