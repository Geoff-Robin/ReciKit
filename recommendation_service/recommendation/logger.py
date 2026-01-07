import logging
import sys
from logging.handlers import RotatingFileHandler
import os


def setup_logger(name: str = None):
    """
    Sets up a centralized logger with console and rotating file handlers.
    """
    logger = logging.getLogger(name)

    # If logger already has handlers, don't add them again
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # Console Handler - Clean output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S"
    )
    console_handler.setFormatter(console_format)

    # File Handler - Detailed and Rotating
    log_file = "mcp_server.log"
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=3,
    )
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_format)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Silence noisy third-party loggers
    silence_loggers = [
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
        "fastapi",
        "mcp",
        "pymongo",
        "qdrant_client",
        "httpx",
        "asyncio",
    ]
    for logger_name in silence_loggers:
        logging.getLogger(logger_name).setLevel(logging.WARNING)

    return logger


# Create a default instance
logger = setup_logger()
