from typing import List

from domain.entities.error_event import ErrorEvent
from domain.ports.event_repository import EventRepository


class InMemoryEventRepository(EventRepository):
    def __init__(self) -> None:
        self._events: List[ErrorEvent] = []

    def save(self, event: ErrorEvent) -> None:
        self._events.append(event)