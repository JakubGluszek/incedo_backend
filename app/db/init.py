import logging
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app import schemas, services
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    init_admin_account(db)
    return


def init_admin_account(db: Session) -> None:
    user_in = schemas.UserCreate(email=settings.FIRST_USER_EMAIL)
    try:
        services.account.create_user(db, user_in=user_in, is_super=True)
        logger.info("Admin initialized")
    except HTTPException as e:
        logger.info("Admin already initialized")
    return
