from src.database.database import init_db
from src.utils.logger import get_logger

logger = get_logger(__name__)

if __name__ == "__main__":
    try:
        logger.info("Starting database initialization")
        init_db()
        logger.info("Database initialization completed successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")