import structlog

from app.core import configure_logger

log = structlog.get_logger()


def main() -> None:
    configure_logger()
    log.info("Started app")
    print("HELLO WORLD AUTH")
