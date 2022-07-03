from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Notebook(Base):
    id: int = Column(Integer, primary_key=True)
    label: str = Column(String(32), nullable=False)
    rank: int = Column(Integer, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    edited_at: datetime = Column(DateTime, default=datetime.utcnow)
    parent_id: int = Column(Integer, nullable=True)
    user_id: int = Column(Integer, nullable=False)

    sections = relationship(
        "Notebook",
        cascade="all,delete",
        foreign_keys=[parent_id],
        primaryjoin="Notebook.id == Notebook.parent_id",
    )

    def __repr__(self):
        return f"id:{self.id}, parent_id:{self.parent_id}, user_id:{self.user_id}"
