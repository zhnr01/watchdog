from datetime import datetime, timedelta, timezone
from uuid import UUID

from jose import jwt


class TokenService:
    def __init__(self, secret_key: str, algorithm: str, access_ttl_minutes: int) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_ttl_minutes = access_ttl_minutes

    def create_access_token(self, user_id: UUID) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": str(user_id),
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=self.access_ttl_minutes)).timestamp()),
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)