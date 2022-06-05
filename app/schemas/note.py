from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator


class NoteCreate(BaseModel):
    title: Optional[str] = None
    body: str


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None


class NoteOut(BaseModel):
    id: int
    title: Optional[str] = None
    body: str
    created_at: datetime
    updated_at: datetime

    @validator("created_at", "updated_at")
    def convert_to_timestamp(cls, v: datetime) -> int:
        return int(v.timestamp())

    class Config:
        orm_mode = True


class Note(BaseModel):
    id: int
    title: Optional[str] = None
    body: str
    created_at: datetime
    updated_at: datetime
    user_id: int
