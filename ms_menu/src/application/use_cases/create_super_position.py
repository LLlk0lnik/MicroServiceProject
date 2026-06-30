from src.application.dtos.super_position_dtos import SuperPositionCreateDTO
from src.domain.entities.super_position import SuperPosition
from src.domain.value_objects.title import Title
from src.domain.value_objects.description import Description
from src.domain.exceptions.domain_exception import PositionNotFound, InvalidSuperPosition
from src.domain.uow.unit_of_work import IUnitOfWork
from datetime import datetime

class CreateSuperPositionUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def execute(self, dto: SuperPositionCreateDTO) -> SuperPosition:
        title_vo = Title(dto.title)
        existing = await self.uow.super_position.get_by_title(title_vo)
        if existing:
            raise ValueError("SuperPosition with this title already exists")

        positions = []
        for pos_id in dto.position_ids:
            pos = await self.uow.position.get_by_id(pos_id)
            if not pos:
                raise PositionNotFound(f"Position with id {pos_id} not found")
            positions.append(pos)

        super_position = SuperPosition(
            id=None,
            title=title_vo,
            description=Description(dto.description) if dto.description else None,
            positions=positions,
            created_at=datetime.now(),
            is_available=True,
        )

        super_position = await self.uow.super_position.add(super_position)
        await self.uow.commit()
        return super_position
