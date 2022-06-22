from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator, Field


class NoteCreate(BaseModel):
    label: str = Field(None, max_length=64)
    notebook_id: int


class NoteUpdate(BaseModel):
    label: Optional[str] = Field(None, max_length=64)
    body: Optional[str] = None
    notebook_id: Optional[int] = None


class Note(BaseModel):
    id: int
    label: Optional[str]
    body: str
    rank: int
    created_at: datetime
    edited_at: datetime
    notebook_id: int
    user_id: int


class NoteOut(BaseModel):
    id: int
    label: str
    body: str
    rank: int
    created_at: int
    edited_at: int
    notebook_id: int

    @validator("created_at", "edited_at", pre=True)
    def convert_to_timestamp(cls, v: datetime) -> int:
        return int(v.timestamp())

    class Config:
        orm_mode = True
