from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

if settings.DEBUG:
    engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
else:
    ssl_args = {"ssl_ca": "/etc/ssl/certs/ca-certificates.crt"}
    engine = create_engine(
        settings.DATABASE_URL, pool_pre_ping=True, connect_args=ssl_args
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
