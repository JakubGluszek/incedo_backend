from pydantic import EmailStr
from sqlalchemy import Column, Integer, String, Boolean

from app.core.config import settings
from app.db.base import Base


class User(Base):
    id: int = Column(Integer, primary_key=True)
    username: str = Column(String(32), nullable=False)
    email: EmailStr = Column(String(255), unique=True, nullable=False)
    password: str = Column(String(255), nullable=False)
    avatar: str = Column(String, server_default=settings.DEFAULT_AVATAR, nullable=False)
    is_super: bool = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"{self.email}"
