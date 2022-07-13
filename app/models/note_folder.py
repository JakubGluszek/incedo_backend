from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class NoteFolder(Base):
    id: int = Column(Integer, primary_key=True)
    label: str = Column(String(32), nullable=False)
    rank: int = Column(Integer, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    edited_at: datetime = Column(DateTime, default=datetime.utcnow)
    parent_id: int = Column(Integer, nullable=True)
    user_id: int = Column(Integer, nullable=False)

    sections = relationship(
        "NoteFolder",
        cascade="all,delete",
        foreign_keys=[parent_id],
        primaryjoin="NoteFolder.id == NoteFolder.parent_id",
    )

    def __repr__(self):
        return f"type: folder, id: {self.id}, parent_id: {self.parent_id}, user_id: {self.user_id};"
