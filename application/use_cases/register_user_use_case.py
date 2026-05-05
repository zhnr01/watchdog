from datetime import datetime, timezone
from uuid import uuid4

from domain.entities.user import User
from domain.ports.user_repository import UserRepository
from domain.services.password_hasher import PasswordHasher


class RegisterUserUseCase:
    def __init__(self, repo: UserRepository, hasher: PasswordHasher) -> None:
        self.repo = repo
        self.hasher = hasher

    def execute(self, email: str, password: str) -> User:
        existing = self.repo.get_by_email(email)
        if existing:
            raise ValueError("Email already registered")

        user = User(
            id=uuid4(),
            email=email,
            password_hash=self.hasher.hash(password),
            is_active=True,
            is_2fa_enabled=False,
            created_at=datetime.now(timezone.utc),
        )
        self.repo.create(user)
        return user