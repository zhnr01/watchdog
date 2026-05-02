from typing import List, Optional

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from domain.entities.error_event import ErrorEvent
from domain.ports.event_repository import EventRepository
from infrastructure.db.mappers.error_event_mapper import ErrorEventMapper
from infrastructure.db.models import ErrorEventModel


class PostgresEventRepository(EventRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, event: ErrorEvent) -> None:
        model = ErrorEventMapper.to_model(event)
        self.session.add(model)
        self.session.commit()

    def list_recent(
        self, limit: int, offset: int, project_id: Optional[str] = None
    ) -> List[ErrorEvent]:
        stmt = select(ErrorEventModel)

        if project_id:
            stmt = stmt.where(ErrorEventModel.project_id == project_id)

        stmt = stmt.order_by(ErrorEventModel.created_at.desc()).limit(limit).offset(offset)

        rows = self.session.execute(stmt).scalars().all()
        return [ErrorEventMapper.to_entity(row) for row in rows]

    def count(self, project_id: Optional[str] = None) -> int:
        stmt = select(func.count(ErrorEventModel.id))
        if project_id:
            stmt = stmt.where(ErrorEventModel.project_id == project_id)
        return self.session.execute(stmt).scalar_one()