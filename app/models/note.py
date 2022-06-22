from typing import Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

from app.db.base import Base


class Note(Base):
    id: int = Column(Integer, primary_key=True)
    label: Optional[str] = Column(String, nullable=True)
    body: str = Column(Text, server_default="", nullable=False)
    rank: int = Column(Integer, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    edited_at: datetime = Column(DateTime, default=datetime.utcnow)
    notebook_id: int = Column(
        Integer, ForeignKey("notebook.id", ondelete="CASCADE"), nullable=True
    )
    user_id: int = Column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", backref=backref("notes", cascade="all, delete"))

    def __repr__(self):
        return f"{self.id}, {self.user_id}"
