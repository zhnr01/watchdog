from abc import ABC, abstractmethod
from typing import Protocol

from domain.entities.error_event import ErrorEvent


class EventRepository(Protocol):
    def save(self, event: ErrorEvent) -> None:
        ...


class EventRepositoryPort(ABC):
    @abstractmethod
    def save(self, event: ErrorEvent) -> None:
        pass