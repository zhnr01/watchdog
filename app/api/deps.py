from functools import lru_cache
from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.settings import settings
from domain.services.fingerprint_service import FingerprintService
from infrastructure.db.session import SessionLocal
from infrastructure.repositories.postgres_event_repository import (
    PostgresEventRepository,
)


def get_db_session() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@lru_cache(maxsize=1)
def get_fingerprint_service() -> FingerprintService:
    return FingerprintService()


def get_event_repository(
    db: Session = Depends(get_db_session),
) -> PostgresEventRepository:
    return PostgresEventRepository(db)