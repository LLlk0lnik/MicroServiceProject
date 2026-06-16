from abc import ABC, abstractmethod
from src.domain.repositories.position_repository import IPositionRepository
from src.domain.repositories.super_position_repository import ISuperPositionRepository

class IUnitOfWork(ABC):
    position: IPositionRepository
    super_position: ISuperPositionRepository

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError
