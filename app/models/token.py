import secrets
from datetime import datetime, timedelta

from pydantic import EmailStr
from sqlalchemy import Column, DateTime, String

from app.core.config import settings
from app.db.base import Base


class Token(Base):
    token: str = Column(String(32), default=secrets.token_urlsafe(16), nullable=False)
    expires: datetime = Column(
        DateTime,
        default=(
            datetime.utcnow() + timedelta(hours=settings.SIGN_IN_TOKEN_EXPIRE_HOURS)
        ),
        nullable=False,
    )
    email: EmailStr = Column(String(256), unique=True, nullable=False)

    @property
    def expired(self) -> bool:
        return self.expires < datetime.utcnow()

    def __repr__(self):
        return f"{self.token}, {self.email}"
