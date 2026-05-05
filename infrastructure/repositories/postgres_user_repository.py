from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities.user import User
from domain.ports.user_repository import UserRepository
from infrastructure.db.auth_models import UserModel
from infrastructure.db.mappers.user_mapper import UserMapper


class PostgresUserRepository(UserRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, user: User) -> None:
        model = UserMapper.to_model(user)
        self.session.add(model)
        self.session.commit()

    def get_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).where(UserModel.email == email)
        row = self.session.execute(stmt).scalars().first()
        return UserMapper.to_entity(row) if row else None

    def get_by_id(self, user_id: UUID) -> User | None:
        stmt = select(UserModel).where(UserModel.id == user_id)
        row = self.session.execute(stmt).scalars().first()
        return UserMapper.to_entity(row) if row else None