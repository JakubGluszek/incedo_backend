import logging

from sqlalchemy.orm import Session

from app import schemas, services
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    # Tables are created using Alembic migrations
    init_admin_account(db)
    return


def init_admin_account(db: Session) -> None:
    user_in = schemas.UserCreate(email=settings.FIRST_USER_EMAIL)
    services.create_user(db, user_in=user_in, is_super=True)
    logger.info("Admin account created")
    return
