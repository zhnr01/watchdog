from domain.entities.user import User
from infrastructure.db.auth_models import UserModel


class UserMapper:
    @staticmethod
    def to_model(entity: User) -> UserModel:
        return UserModel(
            id=entity.id,
            email=entity.email,
            password_hash=entity.password_hash,
            is_active=entity.is_active,
            is_2fa_enabled=entity.is_2fa_enabled,
            created_at=entity.created_at,
        )

    @staticmethod
    def to_entity(model: UserModel) -> User:
        return User(
            id=model.id,
            email=model.email,
            password_hash=model.password_hash,
            is_active=model.is_active,
            is_2fa_enabled=model.is_2fa_enabled,
            created_at=model.created_at,
        )