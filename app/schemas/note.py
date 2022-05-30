from datetime import datetime
from typing import Optional
from pydantic import BaseModel


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

    class Config:
        orm_mode = True


class Note(BaseModel):
    id: int
    title: Optional[str] = None
    body: str
    created_at: datetime
    updated_at: datetime
    user_id: int
