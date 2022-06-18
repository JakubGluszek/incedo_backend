from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator, Field


class NoteCreate(BaseModel):
    label: str = Field(..., max_length=64)
    body: Optional[str] = None
    notebook_id: int


class NoteUpdate(BaseModel):
    label: Optional[str] = Field(None, max_length=64)
    body: Optional[str] = None
    notebook_id: Optional[int] = None


class Note(BaseModel):
    id: int
    label: Optional[str]
    body: str
    notebook_id: int
    created_at: datetime
    updated_at: datetime
    user_id: int


class NoteOut(BaseModel):
    id: int
    label: str
    body: str
    notebook_id: int
    created_at: int
    updated_at: int
    
    @validator("created_at", "updated_at", pre=True)
    def convert_to_timestamp(cls, v: datetime) -> int:
        return int(v.timestamp())

    class Config:
        orm_mode = True
