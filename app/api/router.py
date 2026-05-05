from fastapi import APIRouter

from app.api.routes.health import health_router
from app.api.routes.ingest import ingest_router
from app.api.routes.events import events_router
from app.api.routes.auth import auth_router


api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health_router, tags=["health"])
api_router.include_router(ingest_router, tags=["ingest"])
api_router.include_router(events_router, tags=["events"])
api_router.include_router(auth_router, tags=["auth"])