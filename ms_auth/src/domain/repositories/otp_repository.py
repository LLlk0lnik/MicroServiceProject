from abc import ABC, abstractmethod
from src.domain.entities.OTP_code import OTP


class IOTPRepository(ABC):
    @abstractmethod
    async def add(self, otp: OTP) -> OTP:
        pass

    @abstractmethod
    async def get_last_unused_by_employee(self, employee_id: int) -> OTP | None:
        pass

    @abstractmethod
    async def update(self, otp: OTP) -> OTP:
        pass
