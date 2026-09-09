import logging
import sys
from typing import Optional


def configure_logging(level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger("ai_operations_agent")
    logger.setLevel(level)
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


logger = configure_logging()
