from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.uow.unit_of_work import IUnitOfWork
from src.core.repositories.employee_repository_impl import EmployeeRepository
from src.core.repositories.otp_repository_impl import OTPRepository
from src.core.repositories.refresh_token_repository_impl import RefreshTokenRepository


class SQLAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.employee = EmployeeRepository(session)
        self.OTP = OTPRepository(session)
        self.RefreshToken = RefreshTokenRepository(session)

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
