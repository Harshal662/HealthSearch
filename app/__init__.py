from __future__ import annotations

import logging
from .config import settings

__version__ = "0.1.0"
__all__ = ["__version__", "settings", "logger"]

logger = logging.getLogger("healthsearch")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s - %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

logger.setLevel(logging.INFO if settings.APP_ENV == "production" else logging.DEBUG)
