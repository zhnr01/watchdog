from uuid import UUID
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from domain.entities.refresh_token import RefreshToken
from domain.ports.refresh_token_repository import RefreshTokenRepository
from infrastructure.db.auth_models import RefreshTokenModel
from infrastructure.db.mappers.refresh_token_mapper import RefreshTokenMapper


class PostgresRefreshTokenRepository(RefreshTokenRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, token: RefreshToken) -> None:
        model = RefreshTokenMapper.to_model(token)
        self.session.add(model)
        self.session.commit()

    def get_active_by_user(self, user_id: UUID) -> RefreshToken | None:
        stmt = select(RefreshTokenModel).where(
            RefreshTokenModel.user_id == user_id,
            RefreshTokenModel.revoked_at.is_(None),
        )
        row = self.session.execute(stmt).scalars().first()
        return RefreshTokenMapper.to_entity(row) if row else None

    def revoke(self, token_id: UUID) -> None:
        stmt = update(RefreshTokenModel).where(
            RefreshTokenModel.id == token_id
        ).values(revoked_at="now()")
        self.session.execute(stmt)
        self.session.commit()

    def get_active_by_hash(self, token_hash: str) -> RefreshToken | None:
        stmt = select(RefreshTokenModel).where(
            RefreshTokenModel.token_hash == token_hash,
            RefreshTokenModel.revoked_at.is_(None),
        )
        row = self.session.execute(stmt).scalars().first()
        return RefreshTokenMapper.to_entity(row) if row else None