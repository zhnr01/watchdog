from abc import ABC, abstractmethod
from typing import Protocol, List

from domain.entities.error_event import ErrorEvent


class EventRepository(Protocol):
    def save(self, event: ErrorEvent) -> None:
        ...

    def list_recent(self, limit: int) -> List[ErrorEvent]:
        ...


class EventRepositoryPort(ABC):
    @abstractmethod
    def save(self, event: ErrorEvent) -> None:
        pass

    @abstractmethod
    def list_recent(self, limit: int) -> List[ErrorEvent]:
        pass