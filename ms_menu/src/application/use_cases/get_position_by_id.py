from src.domain.entities.position import Position
from src.domain.exceptions.domain_exception import PositionNotFound
from src.domain.uow.unit_of_work import IUnitOfWork

class GetPositionByIdUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def execute(self, position_id: int) -> Position:
        position = await self.uow.position.get_by_id(position_id)
        if not position:
            raise PositionNotFound(f"Position with id {position_id} not found")
        return position