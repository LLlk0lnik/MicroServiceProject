from src.application.dtos.super_position_dtos import SuperPositionUpdateDTO
from src.domain.entities.super_position import SuperPosition
from src.domain.value_objects.title import Title
from src.domain.value_objects.description import Description
from src.domain.exceptions.domain_exception import PositionNotFound, InvalidSuperPosition
from src.domain.uow.unit_of_work import IUnitOfWork

class UpdateSuperPositionUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def execute(self, super_position_id: int, dto: SuperPositionUpdateDTO) -> SuperPosition:
        super_position = await self.uow.superposition.get_by_id(super_position_id)
        if not super_position:
            raise ValueError(f"SuperPosition with id {super_position_id} not found")

        if dto.title is not None:
            new_title = Title(dto.title)
            existing = await self.uow.superposition.get_by_title(new_title)
            if existing and existing.id != super_position_id:
                raise ValueError("SuperPosition with this title already exists")
            super_position.title = new_title

        if dto.description is not None:
            super_position.description = Description(dto.description) if dto.description else None

        if dto.position_ids is not None:
            new_positions = []
            for pos_id in dto.position_ids:
                pos = await self.uow.position.get_by_id(pos_id)
                if not pos:
                    raise PositionNotFound(f"Position with id {pos_id} not found")
                new_positions.append(pos)

            if not new_positions:
                raise InvalidSuperPosition("SuperPosition must have at least one position")

            first_currency = new_positions[0].price.currency
            for p in new_positions[1:]:
                if p.price.currency != first_currency:
                    raise InvalidSuperPosition("All positions must have same currency")

            super_position.positions = new_positions

        if dto.is_available is not None:
            super_position.is_available = dto.is_available

        super_position = await self.uow.superposition.update(super_position)
        await self.uow.commit()
        return super_position