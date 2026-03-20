import logging
import sys
from pathlib import Path

# ANSI colors
COLORS = {
    "DEBUG": "\033[36m",   # Cyan
    "INFO": "\033[32m",    # Green
    "WARNING": "\033[33m", # Yellow
    "ERROR": "\033[31m",   # Red
    "CRITICAL": "\033[41m" # Red background
}
RESET = "\033[0m"

class ColorFormatter(logging.Formatter):
    def format(self, record):
        level_color = COLORS.get(record.levelname, "")
        record.levelname = f"{level_color}{record.levelname}{RESET}"
        return super().format(record)

def get_logger(name: str, debug: bool = False) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.DEBUG if debug else logging.INFO)
    console.setFormatter(ColorFormatter(
        "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
        "%H:%M:%S"
    ))
    logger.addHandler(console)

    # File handler
    log_file = Path("netgrid.log")
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
        "%Y-%m-%d %H:%M:%S"
    ))
    logger.addHandler(file_handler)

    return logger
