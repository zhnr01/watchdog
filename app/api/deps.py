from functools import lru_cache
from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.settings import settings
from domain.services.fingerprint_service import FingerprintService
from domain.services.password_hasher import PasswordHasher
from domain.services.token_service import TokenService
from infrastructure.db.session import SessionLocal
from infrastructure.repositories.postgres_event_repository import (
    PostgresEventRepository,
)
from infrastructure.repositories.postgres_user_repository import PostgresUserRepository
from infrastructure.repositories.postgres_refresh_token_repository import PostgresRefreshTokenRepository


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

@lru_cache(maxsize=1)
def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()

@lru_cache(maxsize=1)
def get_token_service() -> TokenService:
    return TokenService(
        secret_key=settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
        access_ttl_minutes=settings.jwt_access_ttl_minutes,
    )

def get_user_repository(
    db: Session = Depends(get_db_session),
) -> PostgresUserRepository:
    return PostgresUserRepository(db)

def get_refresh_token_repository(
    db: Session = Depends(get_db_session),
) -> PostgresRefreshTokenRepository:
    return PostgresRefreshTokenRepository(db)