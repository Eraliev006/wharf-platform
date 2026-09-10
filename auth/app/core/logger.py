from typing import Any

import structlog


def configure_logger() -> None:
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(utc=True, fmt="iso"),
            structlog.processors.format_exc_info,
            structlog.dev.ConsoleRenderer(),
        ],
    )


def get_logger() -> Any:
    return structlog.get_logger()
