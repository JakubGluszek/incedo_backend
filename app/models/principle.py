from sqlalchemy import Column, DateTime, String, Integer
from datetime import datetime

from app.db.base import Base


class Principle(Base):
    id = Column(Integer, primary_key=True)
    body = Column(String(512), nullable=False)
    rank = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, nullable=False)
