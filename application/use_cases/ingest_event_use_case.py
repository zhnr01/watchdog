from datetime import datetime
from uuid import uuid4

from app.schemas.ingest import IngestEventRequest, IngestEventResponse
from domain.entities.error_event import ErrorEvent
from domain.ports.event_repository import EventRepository
from domain.services.fingerprint_service import FingerprintService


class IngestEventUseCase:
    def __init__(
        self,
        repository: EventRepository,
        fingerprint_service: FingerprintService,
    ) -> None:
        self.repository = repository
        self.fingerprint_service = fingerprint_service

    def execute(self, request: IngestEventRequest) -> IngestEventResponse:
        fingerprint = self.fingerprint_service.create(
            message=request.message,
            stack_trace=request.stack_trace,
        )

        event = ErrorEvent(
            id=uuid4(),
            project_id=request.project_id,
            fingerprint=fingerprint,
            severity=request.severity,
            message=request.message,
            stack_trace=request.stack_trace,
            metadata=request.metadata,
            created_at=datetime.utcnow(),
        )

        self.repository.save(event)

        return IngestEventResponse(
            event_id=event.id,
            fingerprint=event.fingerprint,
            created_at=event.created_at,
        )