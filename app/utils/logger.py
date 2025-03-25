import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Create logs directory if it doesn't exist
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Configure logging format
log_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.

    Args:
        name: The name of the logger (typically __name__ from the calling module)

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)

    # Only add handlers if the logger doesn't have any
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_format)
        logger.addHandler(console_handler)

        # File handler with rotation
        file_handler = RotatingFileHandler(
            filename=log_dir / "app.log",
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding="utf-8"
        )
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)

    return logger

# Create a default logger instance
logger = get_logger("flight_agent")
