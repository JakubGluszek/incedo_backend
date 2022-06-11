from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator, Field


class NoteCreate(BaseModel):
    title: Optional[str] = Field(None, max_length=64)
    body: str
    folder_id: Optional[int] = None


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=64)
    body: Optional[str] = None
    folder_id: Optional[int] = None


class Note(BaseModel):
    id: int
    title: Optional[str]
    body: str
    folder_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    user_id: int


class NoteOut(BaseModel):
    id: int
    title: Optional[str]
    body: str
    folder_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    @validator("created_at", "updated_at")
    def convert_to_timestamp(cls, v: datetime) -> int:
        return int(v.timestamp())

    class Config:
        orm_mode = True
