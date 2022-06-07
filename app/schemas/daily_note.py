from datetime import datetime
from pydantic import BaseModel, validator


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
    date: datetime

    @validator("date")
    def convert_to_timestamp(cls, v: datetime) -> int:
        return int(v.timestamp())
