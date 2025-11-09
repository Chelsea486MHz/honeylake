import logging
import os
from typing import Optional


def setup_logging(name: str = __name__, level: int = logging.INFO) -> logging.Logger:
    logging.basicConfig(
        level=level,
        format='[%(asctime)s] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(name)


def get_env_str(key: str, default: str = "") -> str:
    return os.getenv(key, default)


def get_env_int(key: str, default: int) -> int:
    try:
        return int(os.getenv(key, str(default)))
    except (ValueError, TypeError):
        return default


def get_env_bool(key: str, default: bool = False) -> bool:
    value = os.getenv(key, "").lower()
    if value in ("true", "1", "yes", "on"):
        return True
    elif value in ("false", "0", "no", "off"):
        return False
    return default
