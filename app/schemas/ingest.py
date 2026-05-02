from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class IngestEventRequest(BaseModel):
    project_id: UUID
    severity: str = Field(min_length=1)
    message: str = Field(min_length=1)
    stack_trace: str = Field(min_length=1)
    metadata: dict = Field(default_factory=dict)


class IngestEventResponse(BaseModel):
    event_id: UUID
    fingerprint: str
    created_at: datetime