from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

from app.db.base import Base


class DailyNote(Base):
    id: int = Column(Integer, primary_key=True)
    body: str = Column(Text, nullable=False)
    date: datetime = Column(DateTime, nullable=False)
    user_id: int = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )

    user = relationship("User", backref=backref("daily_notes", cascade="all, delete"))

    def __repr__(self):
        return f"{self.id}, {self.user_id}"
