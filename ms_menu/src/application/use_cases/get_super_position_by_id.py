from src.domain.entities.super_position import SuperPosition
from src.domain.uow.unit_of_work import IUnitOfWork

class GetSuperPositionByIdUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def execute(self, super_position_id: int) -> SuperPosition:
        super_position = await self.uow.superposition.get_by_id(super_position_id)
        if not super_position:
            raise ValueError(f"SuperPosition with id {super_position_id} not found")
        return super_position