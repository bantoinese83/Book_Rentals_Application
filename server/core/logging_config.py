# logging_config.py
import sys

from loguru import logger
from datetime import datetime
import os

LOGS_DIR = "logs"


def setup_logging():
    # Create logs directory if it doesn't exist
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)

    # Remove all previous handlers
    logger.remove()

    # Add a default handler for all levels
    logger.add(
        sink=os.path.join(LOGS_DIR, "{time:YYYY-MM-DD}.log"),
        level="DEBUG",
        format="{time} - {name} - {level} - {message}",
        rotation="1 week",
        compression="zip",
    )

    # Add additional handlers for specific levels
    add_handler(LOGS_DIR, "DEBUG", "debug")
    add_handler(LOGS_DIR, "WARNING", "warning")
    add_handler(LOGS_DIR, "ERROR", "error")

    # Add a handler to log to console
    logger.add(
        sink=sys.stderr,
        level="DEBUG",
        format="{time} - {name} - {level} - {message}"
    )

    return logger


def add_handler(logs_dir, level, filename):
    logger.add(
        sink=os.path.join(logs_dir, f"{filename}_{datetime.now():%Y-%m-%d}.log"),
        level=level,
        format="{time} - {name} - {level} - {message}",
        rotation="1 week",
        compression="zip",
    )
