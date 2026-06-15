from abc import ABC, abstractmethod
from ms_menu.src.domain.repositories.position_repository import IPositionRepository
from ms_menu.src.domain.repositories.super_position_repository import ISuperPositionRepository

class IUnitOfWork(ABC):
    position: IPositionRepository
    super_position: ISuperPositionRepository

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError
