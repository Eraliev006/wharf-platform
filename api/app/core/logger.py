import logging
from typing import Any

import structlog

from app.core.settings import settings


def configure_logger() -> None:
    log_maps = logging.getLevelNamesMapping()
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(utc=True, fmt="iso"),
            # DO NOT USE WITH CONSOLE READERER ONLY WITH JSON
            # structlog.processors.format_exc_info,
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            log_maps[settings.log_level]
        ),
    )


def get_logger() -> Any:
    return structlog.get_logger()
