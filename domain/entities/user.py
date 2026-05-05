from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class User:
    id: UUID
    email: str
    password_hash: str
    is_active: bool
    is_2fa_enabled: bool
    created_at: datetime