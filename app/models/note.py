from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.db.base import Base


class Note(Base):
    id: int = Column(Integer, primary_key=True)
    label: Optional[str] = Column(String(64), nullable=True)
    body: str = Column(Text, nullable=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    edited_at: datetime = Column(DateTime, default=datetime.utcnow)
    user_id: int = Column(Integer, nullable=False)

    def __repr__(self):
        return f"id: {self.id}, user_id: {self.user_id}"
