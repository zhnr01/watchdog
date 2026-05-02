from typing import List, Optional

from app.schemas.events import EventItem, ListEventsResponse
from domain.entities.error_event import ErrorEvent
from domain.ports.event_repository import EventRepository


class ListEventsUseCase:
    def __init__(self, repository: EventRepository) -> None:
        self.repository = repository

    def execute(
        self, page: int, page_size: int, project_id: Optional[str] = None
    ) -> ListEventsResponse:
        offset = (page - 1) * page_size
        events: List[ErrorEvent] = self.repository.list_recent(
            limit=page_size, offset=offset, project_id=project_id
        )
        total = self.repository.count(project_id=project_id)

        items = [
            EventItem(
                id=e.id,
                project_id=e.project_id,
                fingerprint=e.fingerprint,
                severity=e.severity,
                message=e.message,
                stack_trace=e.stack_trace,
                metadata=e.metadata,
                created_at=e.created_at,
            )
            for e in events
        ]
        return ListEventsResponse(items=items, page=page, page_size=page_size, total=total)