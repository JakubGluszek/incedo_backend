import logging

from app.db.init import init_db
from app.db.session import SessionLocal

logger = logging.getLogger(__name__)


def init() -> None:
    logger.info("Data initialization")
    db = SessionLocal()
    init_db(db)
    db.close()
    logger.info("Data initialized")


def main() -> None:
    init()


if __name__ == "__main__":
    main()
