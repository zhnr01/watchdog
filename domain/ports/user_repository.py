from typing import Protocol
from uuid import UUID

from domain.entities.user import User


class UserRepository(Protocol):
    def create(self, user: User) -> None: ...
    def get_by_email(self, email: str) -> User | None: ...
    def get_by_id(self, user_id: UUID) -> User | None: ...