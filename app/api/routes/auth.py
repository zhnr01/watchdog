from datetime import datetime, timedelta, timezone
import hashlib
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_password_hasher, get_token_service
from app.schemas.auth import RefreshRequest, RegisterRequest, LoginRequest, TokenResponse
from application.use_cases.register_user_use_case import RegisterUserUseCase
from application.use_cases.login_use_case import LoginUseCase
from application.use_cases.rotate_refresh_token_use_case import RotateRefreshTokenUseCase
from domain.entities.refresh_token import RefreshToken
from infrastructure.repositories.postgres_user_repository import PostgresUserRepository
from infrastructure.repositories.postgres_refresh_token_repository import PostgresRefreshTokenRepository
from app.api.deps import get_user_repository, get_refresh_token_repository


auth_router = APIRouter()


def _hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


@auth_router.post("/auth/register", response_model=TokenResponse, status_code=201)
def register(
    payload: RegisterRequest,
    users: PostgresUserRepository = Depends(get_user_repository),
    refresh_tokens: PostgresRefreshTokenRepository = Depends(get_refresh_token_repository),
    hasher=Depends(get_password_hasher),
    token_service=Depends(get_token_service),
) -> TokenResponse:
    use_case = RegisterUserUseCase(users, hasher)
    user = use_case.execute(payload.email, payload.password)

    refresh_token = token_service.create_refresh_token()
    refresh_hash = _hash_refresh_token(refresh_token)

    refresh_use_case = RotateRefreshTokenUseCase(refresh_tokens)
    refresh_use_case.execute(
        user_id=user.id,
        token_hash=refresh_hash,
        expires_at=datetime.now(timezone.utc) + timedelta(days=30),
    )

    access_token = token_service.create_access_token(user.id)

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@auth_router.post("/auth/login", response_model=TokenResponse)
def login(
    payload: LoginRequest,
    users: PostgresUserRepository = Depends(get_user_repository),
    refresh_tokens: PostgresRefreshTokenRepository = Depends(get_refresh_token_repository),
    hasher=Depends(get_password_hasher),
    token_service=Depends(get_token_service),
) -> TokenResponse:
    use_case = LoginUseCase(users, hasher)

    try:
        user = use_case.execute(payload.email, payload.password)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    refresh_token = token_service.create_refresh_token()
    refresh_hash = _hash_refresh_token(refresh_token)

    refresh_use_case = RotateRefreshTokenUseCase(refresh_tokens)
    refresh_use_case.execute(
        user_id=user.id,
        token_hash=refresh_hash,
        expires_at=datetime.now(timezone.utc) + timedelta(days=30),
    )

    access_token = token_service.create_access_token(user.id)

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@auth_router.post("/auth/refresh", response_model=TokenResponse)
def refresh(
    payload: RefreshRequest,
    refresh_tokens: PostgresRefreshTokenRepository = Depends(get_refresh_token_repository),
    users: PostgresUserRepository = Depends(get_user_repository),
    token_service=Depends(get_token_service),
) -> TokenResponse:
    refresh_hash = _hash_refresh_token(payload.refresh_token)

    token_record = refresh_tokens.get_active_by_hash(refresh_hash)
    if token_record is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    if token_record.expires_at < datetime.now(timezone.utc):
        refresh_tokens.revoke(token_record.id)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")

    user = users.get_by_id(token_record.user_id)
    if user is None or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not active")

    # Rotate refresh token
    new_refresh = token_service.create_refresh_token()
    refresh_hash = _hash_refresh_token(new_refresh)

    refresh_use_case = RotateRefreshTokenUseCase(refresh_tokens)
    refresh_use_case.execute(
        user_id=user.id,
        token_hash=refresh_hash,
        expires_at=datetime.now(timezone.utc) + timedelta(days=30),
    )

    access_token = token_service.create_access_token(user.id)

    return TokenResponse(access_token=access_token, refresh_token=new_refresh)