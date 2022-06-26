from sqlalchemy import Column, Integer

from app.db.base import Base


class UserSettings(Base):
    id: int = Column(Integer, primary_key=True)
    time_diff: int = Column(Integer, nullable=True)
    user_id: int = Column(Integer, nullable=False)
