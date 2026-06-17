from src.domain.entities.position import Position
from src.domain.uow.unit_of_work import IUnitOfWork

class GetPositionsNotInSuperPositionUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def execute(self, super_position_id: int) -> list[Position]:
        positions = await self.uow.superposition.get_positions_not_in_super(super_position_id)
        return positions