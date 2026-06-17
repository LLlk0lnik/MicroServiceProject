from src.domain.entities.position import Position
from src.domain.value_objects.category import Category
from src.domain.uow.unit_of_work import IUnitOfWork

class GetPositionsUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def execute(
        self,
        category: str | None = None,
        is_available: bool | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> tuple[list[Position], int]:
        category_vo = Category(category) if category else None
        positions, total = await self.uow.position.get_filtered(
            category=category_vo,
            is_available=is_available,
            limit=limit,
            offset=offset
        )
        return positions, total