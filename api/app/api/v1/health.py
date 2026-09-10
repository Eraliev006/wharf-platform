from typing import Any

from fastapi import status
from fastapi.routing import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", status_code=status.HTTP_200_OK)
async def health() -> dict[str, Any]:
    return {"status": "healthy"}
