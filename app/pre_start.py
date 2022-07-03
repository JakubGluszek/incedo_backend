import logging

from app.db.utils import check_db_connected

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init():
    check_db_connected()


def main() -> None:
    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
