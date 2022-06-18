from typing import Optional
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Notebook(Base):
    id: int = Column(Integer, primary_key=True)
    label: str = Column(String, nullable=False)
    rank: int = Column(Integer, nullable=False)
    about: Optional[str] = Column(String, nullable=True)
    user_id: int = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )

    notes = relationship("Note", backref="notebook", cascade="all, delete")

    def __str__(self):
        return f"Folder: {self.label}"
