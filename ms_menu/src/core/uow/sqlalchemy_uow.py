from sqlalchemy.ext.asyncio import AsyncSession
from ms_menu.src.domain.uow.unit_of_work import IUnitOfWork
from ms_menu.src.core.repositories.position_repository_impl import PositionRepository
from ms_menu.src.core.repositories.super_position_repository_impl import SuperPositionRepository


class SQLAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.position = PositionRepository(session)
        self.superposition = SuperPositionRepository(session)

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
