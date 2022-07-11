from sqlalchemy import Column, Integer, String

from app.db.base import Base


class Theme(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    user_id = Column(Integer, nullable=True)
    primary = Column(String(7), nullable=False)
    secondary = Column(String(7), nullable=False)
    accent = Column(String(7), nullable=False)
    neutral = Column(String(7), nullable=False)
    base = Column(String(7), nullable=False)
    info = Column(String(7), nullable=False)
    success = Column(String(7), nullable=False)
    warning = Column(String(7), nullable=False)
    error = Column(String(7), nullable=False)
