from domain.ports.user_repository import UserRepository
from domain.services.password_hasher import PasswordHasher


class LoginUseCase:
    def __init__(self, repo: UserRepository, hasher: PasswordHasher) -> None:
        self.repo = repo
        self.hasher = hasher

    def execute(self, email: str, password: str):
        user = self.repo.get_by_email(email)
        if user is None:
            raise ValueError("Invalid credentials")
        if not self.hasher.verify(password, user.password_hash):
            raise ValueError("Invalid credentials")
        return user