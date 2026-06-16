from abc import ABC, abstractmethod
from ms_menu.src.domain.entities.position import Position
from ms_menu.src.domain.value_objects.title import Title
from ms_menu.src.domain.value_objects.category import Category

class IPositionRepository(ABC):

    @abstractmethod
    async def get_by_id(self, position_id: int) -> Position | None:
        pass

    @abstractmethod
    async def get_by_title(self, title: Title) -> Position | None:
        pass

    @abstractmethod
    async def get_by_category(self, category: Category) -> list[Position]:
        pass

    @abstractmethod
    async def get_all_avaliable(self) -> list[Position]:
        pass

    @abstractmethod
    async def add(self, position: Position) -> Position:
        pass

    @abstractmethod
    async def delete(self, position_id: int) -> None:
        pass

    @abstractmethod
    async def update(self, position: Position) -> Position:
        pass

    @abstractmethod
    async def exists_by_title(self, title: Title) -> bool:
        pass

    @abstractmethod
    async def get_filtered(
            self,
            category: Category | None = None,
            is_available: bool | None = None,
            limit: int = 100,
            offset: int = 0
    ) -> tuple[list[Position], int]:
        pass
