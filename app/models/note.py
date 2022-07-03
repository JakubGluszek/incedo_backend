from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import backref, relationship

from app.db.base import Base


class Note(Base):
    id: int = Column(Integer, primary_key=True)
    label: Optional[str] = Column(String(64), nullable=True)
    body: str = Column(Text, nullable=True)
    rank: int = Column(Integer, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    edited_at: datetime = Column(DateTime, default=datetime.utcnow)
    note_folder_id: int = Column(Integer, nullable=True)
    user_id: int = Column(Integer, nullable=False)

    note_folder = relationship(
        "NoteFolder",
        backref=backref("notes"),
        foreign_keys=[note_folder_id],
        primaryjoin="NoteFolder.id == Note.note_folder_id",
    )

    def __repr__(self):
        return f"{self.id}, {self.user_id}"
