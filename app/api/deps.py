from functools import lru_cache

from domain.services.fingerprint_service import FingerprintService
from infrastructure.repositories.in_memory_event_repository import (
    InMemoryEventRepository,
)


@lru_cache(maxsize=1)
def get_event_repository() -> InMemoryEventRepository:
    return InMemoryEventRepository()


@lru_cache(maxsize=1)
def get_fingerprint_service() -> FingerprintService:
    return FingerprintService()