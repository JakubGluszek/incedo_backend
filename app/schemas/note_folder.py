from typing import Optional
from pydantic import BaseModel


class NoteFolderCreate(BaseModel):
    label: Optional[str] = None
    parent_id: Optional[int] = None


class NoteFolderUpdate(BaseModel):
    label: Optional[str] = None
    parent_id: Optional[int] = None


class NoteFolder(BaseModel):
    id: int
    label: str
    parent_id: Optional[int]
    user_id: int


class NoteFolderOut(BaseModel):
    id: int
    label: str
    parent_id: Optional[int]
