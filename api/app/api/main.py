from fastapi.routing import APIRouter

from app.core import settings

from .v1.health import router as health_router

router = APIRouter(prefix=f"/api/{settings.api_version}")

router.include_router(health_router)
