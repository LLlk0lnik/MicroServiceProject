from ms_menu.src.domain.uow.unit_of_work import IUnitOfWork

class DeletePositionUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def execute(self, position_id: int) -> None:
        await self.uow.position.delete(position_id)
        await self.uow.commit()