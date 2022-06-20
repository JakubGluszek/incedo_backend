from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field


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
    user_id: int


class NotebookOut(BaseModel):
    id: int
    label: str
    rank: int
    about: Optional[str] = None
    notes: List[NoteOut]

    class Config:
        orm_mode = True


from app.schemas import NoteOut

NotebookOut.update_forward_refs()
