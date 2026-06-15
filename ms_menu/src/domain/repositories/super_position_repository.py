from abc import ABC, abstractmethod
from typing import List, Optional
from ms_menu.src.domain.entities.super_position import SuperPosition
from ms_menu.src.domain.value_objects.title import Title

class ISuperPositionRepository(ABC):

    @abstractmethod
    async def get_by_id(self, super_position_id: int) -> Optional[SuperPosition]:
        pass

    @abstractmethod
    async def get_by_title(self, title: Title) -> Optional[SuperPosition]:
        pass

    @abstractmethod
    async def get_all_available(self) -> List[SuperPosition]:
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
    async def get_position_not_in_super(self, super_position_id: int) -> List[SuperPosition]:
        pass
    