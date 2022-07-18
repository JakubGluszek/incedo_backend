from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class NoteCreate(BaseModel):
    label: str = Field(..., max_length=64)
    body: Optional[str] = ""


class NoteUpdate(BaseModel):
    label: Optional[str] = Field(None, max_length=64)
    body: Optional[str] = None


class Note(BaseModel):
    id: int
    label: Optional[str]
    body: str
    created_at: datetime
    edited_at: datetime
    user_id: int


class NoteOut(BaseModel):
    id: int
    label: str
    body: str
    created_at: int
    edited_at: int

    @validator("created_at", "edited_at", pre=True)
    def convert_to_timestamp(cls, v: datetime) -> int:
        return int(v.timestamp())

    class Config:
        orm_mode = True
