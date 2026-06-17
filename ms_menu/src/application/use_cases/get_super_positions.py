from src.domain.entities.super_position import SuperPosition
from src.domain.uow.unit_of_work import IUnitOfWork

class GetSuperPositionsUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def execute(
        self,
        is_available: bool | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> tuple[list[SuperPosition], int]:
        super_positions, total = await self.uow.superposition.get_filtered(
            is_available=is_available,
            limit=limit,
            offset=offset
        )
        return super_positions, total