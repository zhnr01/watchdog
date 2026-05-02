from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class EventItem(BaseModel):
    id: UUID
    project_id: UUID
    fingerprint: str
    severity: str
    message: str
    stack_trace: str
    metadata: dict
    created_at: datetime


class ListEventsResponse(BaseModel):
    items: list[EventItem]
    page: int
    page_size: int
    total: int