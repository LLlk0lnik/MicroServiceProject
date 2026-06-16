from src.domain.uow.unit_of_work import IUnitOfWork

class DeleteSuperPositionUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def execute(self, super_position_id: int) -> None:
        await self.uow.superposition.delete(super_position_id)
        await self.uow.commit()