from dataclasses import dataclass
from datetime import datetime, timedelta
from src.domain.exceptions.domain_exceptions import (
    OTPExpiredException,
    OTPInvalidException,
    OTPMaxAttemptsExceeded,
)


@dataclass
class OTP:
    id: int | None
    employee_id: int
    code: str
    expires_at: datetime
    attempts: int
    is_used: bool
    created_at: datetime

    MAX_ATTEMPTS = 5
    VALIDITY_SECONDS = 300

    @classmethod
    def create(cls, employee_id: int, code_value: str) -> "OTP":
        now = datetime.now()
        return OTP(
            id=None,
            employee_id=employee_id,
            code=code_value,
            expires_at=now + timedelta(seconds=cls.VALIDITY_SECONDS),
            attempts=0,
            is_used=False,
            created_at=now,
        )

    def verify(self, input_code: str) -> bool:
        if self.is_used:
            raise OTPInvalidException()
        if datetime.now() > self.expires_at:
            raise OTPExpiredException()
        if self.attempts >= self.MAX_ATTEMPTS:
            raise OTPMaxAttemptsExceeded()

        self.attempts += 1
        if self.code == input_code:
            self.is_used = True
            return True
        return False
