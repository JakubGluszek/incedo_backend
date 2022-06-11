from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from app.db.base import Base


class UserSettings(Base):
    id: int = Column(Integer, primary_key=True)
    time_diff: int = Column(Integer, nullable=True)
    user_id: int = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )

    user = relationship(
        "User", backref=backref("settings", cascade="all, delete", uselist=False)
    )
