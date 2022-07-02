from typing import Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship, backref

from app.db.base import Base


class Note(Base):
    id: int = Column(Integer, primary_key=True)
    label: Optional[str] = Column(String(64), nullable=True)
    body: str = Column(Text, nullable=True)
    rank: int = Column(Integer, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    edited_at: datetime = Column(DateTime, default=datetime.utcnow)
    notebook_id: int = Column(Integer, nullable=True)
    user_id: int = Column(Integer, nullable=False)

    notebook = relationship(
        "Notebook",
        backref=backref("notes"),
        foreign_keys=[notebook_id],
        primaryjoin="Notebook.id == Note.notebook_id",
    )

    def __repr__(self):
        return f"{self.id}, {self.user_id}"
