from functools import lru_cache
from typing import Generator

from fastapi import Depends
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.settings import settings
from domain.services.fingerprint_service import FingerprintService
from domain.services.password_hasher import PasswordHasher
from domain.services.token_service import TokenService
from domain.entities.user import User
from infrastructure.db.session import SessionLocal
from infrastructure.repositories.postgres_event_repository import (
    PostgresEventRepository,
)
from infrastructure.repositories.postgres_user_repository import PostgresUserRepository
from infrastructure.repositories.postgres_refresh_token_repository import PostgresRefreshTokenRepository

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


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


def get_current_user(
    token: str = Depends(oauth2_scheme),
    users: PostgresUserRepository = Depends(get_user_repository),
    token_service=Depends(get_token_service),
) -> User:
    user_id = token_service.decode_access_token(token)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = users.get_by_id(user_id)
    if user is None or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not active")
    return user