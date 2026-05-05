from datetime import datetime, timezone
from uuid import uuid4

from domain.entities.refresh_token import RefreshToken
from domain.ports.refresh_token_repository import RefreshTokenRepository


class RotateRefreshTokenUseCase:
    def __init__(self, repo: RefreshTokenRepository) -> None:
        self.repo = repo

    def execute(self, user_id, token_hash: str, expires_at) -> RefreshToken:
        existing = self.repo.get_active_by_user(user_id)
        if existing:
            self.repo.revoke(existing.id)

        new_token = RefreshToken(
            id=uuid4(),
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            revoked_at=None,
            created_at=datetime.now(timezone.utc),
        )
        self.repo.create(new_token)
        return new_token