from dataclasses import dataclass
from datetime import datetime


@dataclass
class RefreshToken:
    id: int | None
    token: str
    employee_id: int
    expires_at: datetime
    is_revoked: bool
    created_at: datetime

    def is_valid(self) -> bool:
        return not self.is_revoked and datetime.now() < self.expires_at

    def revoke(self) -> None:
        self.is_revoked = True
