from typing import Protocol
from uuid import UUID

from domain.entities.refresh_token import RefreshToken


class RefreshTokenRepository(Protocol):
    def create(self, token: RefreshToken) -> None: ...
    def get_active_by_user(self, user_id: UUID) -> RefreshToken | None: ...
    def revoke(self, token_id: UUID) -> None: ...