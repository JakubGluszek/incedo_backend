import secrets
from pydantic import EmailStr
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime, timedelta

from app.core.config import settings
from app.db.base import Base


class User(Base):
    id: int = Column(Integer, primary_key=True)
    username: str = Column(String(32), server_default="hooman", nullable=False)
    email: EmailStr = Column(String(255), unique=True, nullable=False)
    avatar: str = Column(String, server_default=settings.DEFAULT_AVATAR, nullable=False)
    is_super: bool = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"{self.email}"