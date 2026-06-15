from abc import ABC, abstractmethod
from typing import List, Optional
from ms_menu.src.domain.entities.position import Position
from ms_menu.src.domain.value_objects.title import Title
from ms_menu.src.domain.value_objects.category import Category

class IPositionRepository(ABC):

    @abstractmethod
    async def get_by_id(self, position_id: int) -> Optional[Position]:
        pass

    @abstractmethod
    async def get_by_title(self, title: Title) -> Optional[Position]:
        pass

    @abstractmethod
    async def get_by_category(self, category: Category) -> List[Position]:
        pass

    @abstractmethod
    async def get_all_avaliable(self) -> List[Position]:
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
    async def exists_by_Title(self, title: Title) -> bool:
        pass
    