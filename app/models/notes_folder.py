from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from app.db.base import Base


class NotesFolder(Base):
    id: int = Column(Integer, primary_key=True)
    label: str = Column(String, nullable=False)
    parent_id: int = Column(
        Integer, ForeignKey("notesfolder.id", ondelete="CASCADE"), nullable=True
    )
    user_id: int = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )

    notes = relationship("Note", backref="folder", cascade="all, delete")
    folders = relationship(
        "NotesFolder",
        backref="parent",
        cascade="all, delete",
        remote_side=[id],
    )

    def __str__(self):
        return f"Folder: {self.label}"
