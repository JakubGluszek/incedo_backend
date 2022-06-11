from typing import Optional
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from app.db.base import Base


class Note(Base):
    id: int = Column(Integer, primary_key=True)
    title: Optional[str] = Column(String, nullable=True)
    body: str = Column(Text, server_default="", nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    note_folder: int = Column(Integer, ForeignKey("notefolder.id"), nullable=False)
    user_id: int = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    
    def __repr__(self):
        return f"{self.id}, {self.user_id}"
