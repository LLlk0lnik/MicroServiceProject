from abc import ABC, abstractmethod
from src.domain.repositories.employee_repository import IEmployeeRepository
from src.domain.repositories.otp_repository import IOTPRepository
from src.domain.repositories.refresh_token_repository import IRefreshTokenRepository


class IUnitOfWork(ABC):
    employee: IEmployeeRepository
    OTP_code: IOTPRepository
    refresh_token: IRefreshTokenRepository

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError
