from domain.entities.error_event import ErrorEvent
from infrastructure.db.models import ErrorEventModel


class ErrorEventMapper:
    @staticmethod
    def to_model(event: ErrorEvent) -> ErrorEventModel:
        return ErrorEventModel(
            id=event.id,
            project_id=event.project_id,
            fingerprint=event.fingerprint,
            severity=event.severity,
            message=event.message,
            stack_trace=event.stack_trace,
            event_metadata=event.metadata,
            created_at=event.created_at,
        )