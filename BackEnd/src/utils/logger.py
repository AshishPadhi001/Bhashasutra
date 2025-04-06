# src/utils/logger.py
import logging
import sys

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger("bhashasutra")


def get_logger(name: str = "bhashasutra") -> logging.Logger:
    """
    Returns a logger with the specified name.
    If no name is provided, defaults to 'bhashasutra'.
    """
    return logging.getLogger(name)
