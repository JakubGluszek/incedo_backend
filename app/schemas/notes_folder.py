from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field


class NotesFolderCreate(BaseModel):
    label: Optional[str] = Field(None, max_length=32)
    parent_id: Optional[int] = None


class NotesFolderUpdate(BaseModel):
    label: Optional[str] = Field(None, max_length=32)
    parent_id: Optional[int] = None


class NotesFolder(BaseModel):
    id: int
    label: str
    parent_id: Optional[int]
    user_id: int


class NotesFolderOut(BaseModel):
    id: int
    label: str
    parent_id: Optional[int]
    notes: List[NoteOut]

    class Config:
        orm_mode = True


from app.schemas import NoteOut

NotesFolderOut.update_forward_refs()
