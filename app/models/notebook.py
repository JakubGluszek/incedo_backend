from datetime import datetime
from typing import Optional
from sqlalchemy import Column, DateTime, String, Integer

from app.db.base import Base


class Notebook(Base):
    id: int = Column(Integer, primary_key=True)
    label: str = Column(String(32), nullable=False)
    rank: int = Column(Integer, nullable=False)
    about: Optional[str] = Column(String(256), nullable=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    edited_at: datetime = Column(DateTime, default=datetime.utcnow)
    user_id: int = Column(Integer, nullable=False)

    def __str__(self):
        return f"Folder: {self.label}"
