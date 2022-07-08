from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class NoteCreate(BaseModel):
    label: str = Field(None, max_length=64)
    body: Optional[str] = ""
    note_folder_id: int


class NoteUpdate(BaseModel):
    label: Optional[str] = Field(None, max_length=64)
    body: Optional[str] = None
    note_folder_id: Optional[int] = None


class Note(BaseModel):
    id: int
    label: Optional[str]
    body: str
    rank: int
    created_at: datetime
    edited_at: datetime
    note_folder_id: Optional[int]
    user_id: int


class NoteOut(BaseModel):
    id: int
    label: str
    body: str
    rank: int
    created_at: int
    edited_at: int
    note_folder_id: Optional[int]

    @validator("created_at", "edited_at", pre=True)
    def convert_to_timestamp(cls, v: datetime) -> int:
        return int(v.timestamp())

    class Config:
        orm_mode = True


class NoteNewRank(BaseModel):
    id: int
    rank: int
    note_folder_id: Optional[int] = None
