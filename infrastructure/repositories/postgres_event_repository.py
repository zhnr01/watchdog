from sqlalchemy.orm import Session

from domain.entities.error_event import ErrorEvent
from domain.ports.event_repository import EventRepository
from infrastructure.db.mappers.error_event_mapper import ErrorEventMapper


class PostgresEventRepository(EventRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, event: ErrorEvent) -> None:
        model = ErrorEventMapper.to_model(event)
        self.session.add(model)
        self.session.commit()