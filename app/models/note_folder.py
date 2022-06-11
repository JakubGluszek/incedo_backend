from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class NoteFolder(Base):
    id: int = Column(Integer, primary_key=True)
    label: str = Column(String, nullable=False)
    parent_id: int = Column(Integer, ForeignKey("notefolder.id"), nullable=True)
    user_id: int = Column(Integer, ForeignKey("user.id"), nullable=False)

    notes = relationship("Note")
    folders = relationship("NoteFolder")
    
    def __str__(self):
        return F"Folder: {self.label}"
