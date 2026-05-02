from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class ErrorEvent:
    id: UUID
    project_id: UUID
    fingerprint: str
    severity: str
    message: str
    stack_trace: str
    metadata: dict
    created_at: datetime