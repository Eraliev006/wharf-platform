from typing import Any

import structlog
from fastapi import status
from fastapi.routing import APIRouter

router = APIRouter(prefix="/health", tags=["health"])

log = structlog.get_logger()


@router.get("/", status_code=status.HTTP_200_OK)
async def health() -> dict[str, Any]:
    log.info("Health endpoint is called")
    return {"status": "healthy"}
