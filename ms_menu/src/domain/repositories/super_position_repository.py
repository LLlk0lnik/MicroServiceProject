from abc import ABC, abstractmethod
from ms_menu.src.domain.entities.super_position import SuperPosition
from ms_menu.src.domain.entities.position import Position
from ms_menu.src.domain.value_objects.title import Title

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
    async def get_position_not_in_super(self, super_position_id: int) -> list[Position]:
        pass

    @abstractmethod
    async def get_filtered(
        self,
        is_available: bool | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> tuple[list[SuperPosition], int]:
        pass
