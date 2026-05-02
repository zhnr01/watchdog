from abc import ABC, abstractmethod
from typing import Protocol, List, Optional

from domain.entities.error_event import ErrorEvent


class EventRepository(Protocol):
    def save(self, event: ErrorEvent) -> None:
        ...

    def list_recent(
        self, limit: int, offset: int, project_id: Optional[str] = None
    ) -> List[ErrorEvent]:
        ...

    def count(self, project_id: Optional[str] = None) -> int:
        ...


class EventRepositoryPort(ABC):
    @abstractmethod
    def save(self, event: ErrorEvent) -> None:
        pass

    @abstractmethod
    def list_recent(
        self, limit: int, offset: int, project_id: Optional[str] = None
    ) -> List[ErrorEvent]:
        pass

    @abstractmethod
    def count(self, project_id: Optional[str] = None) -> int:
        pass