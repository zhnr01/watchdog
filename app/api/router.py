from fastapi import APIRouter

from app.api.routes.health import health_router
from app.api.routes.ingest import ingest_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health_router, tags=["health"])
api_router.include_router(ingest_router, tags=["ingest"])