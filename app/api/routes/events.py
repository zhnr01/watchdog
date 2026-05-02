from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.api.deps import get_event_repository
from app.schemas.events import ListEventsResponse
from application.use_cases.list_events_use_case import ListEventsUseCase

events_router = APIRouter()


@events_router.get("/events", response_model=ListEventsResponse)
def list_events(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
    project_id: Optional[str] = Query(default=None),
    repository=Depends(get_event_repository),
) -> ListEventsResponse:
    use_case = ListEventsUseCase(repository)
    return use_case.execute(page=page, page_size=page_size, project_id=project_id)