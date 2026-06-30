from abc import ABC, abstractmethod
from src.domain.entities.super_position import SuperPosition
from src.domain.entities.position import Position
from src.domain.value_objects.title import Title

class ISuperPositionRepository(ABC):

    @abstractmethod
    async def get_by_id(self, super_position_id: int) -> SuperPosition | None:
        pass

    @abstractmethod
    async def get_by_title(self, title: Title) -> SuperPosition | None:
        pass

    @abstractmethod
    async def get_all_available(self) -> list[SuperPosition]:
        pass

    @abstractmethod
    async def add(self, super_position: SuperPosition) -> SuperPosition:
        pass

    @abstractmethod
    async def delete(self, super_position_id: int) -> None:
        pass

    @abstractmethod
    async def update(self, super_position: SuperPosition) -> SuperPosition:
        pass

    @abstractmethod
    async def exists_by_title(self, title: Title) -> bool:
        pass

    @abstractmethod
    async def get_positions_not_in_super(self, super_position_id: int) -> list[Position]:
        pass

    async def get_position_not_in_super(self, super_position_id: int) -> list[Position]:
        return await self.get_positions_not_in_super(super_position_id)

    @abstractmethod
    async def get_filtered(
        self,
        is_available: bool | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> tuple[list[SuperPosition], int]:
        pass
