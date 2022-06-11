from datetime import datetime
from pydantic import BaseModel


class DailyNoteCreate(BaseModel):
    body: str


class DailyNoteUpdate(BaseModel):
    body: str


class DailyNote(BaseModel):
    id: int
    body: str
    date: datetime
    user_id: int


class DailyNoteOut(BaseModel):
    id: int
    body: str

    class Config:
        orm_mode = True
