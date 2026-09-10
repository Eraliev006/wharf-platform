from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

from app.core import configure_logger

from .api.main import router

log = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    configure_logger()

    log.info("Application started")
    yield

    log.info("Application ended")


app = FastAPI(lifespan=lifespan)  # pyright: ignore[reportArgumentType]


app.include_router(router)
