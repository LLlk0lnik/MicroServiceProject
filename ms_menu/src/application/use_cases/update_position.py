from src.application.dtos.position_dtos import PositionUpdateDTO
from src.domain.entities.position import Position
from src.domain.value_objects.title import Title
from src.domain.value_objects.price import Price
from src.domain.value_objects.description import Description
from src.domain.value_objects.category import Category
from src.domain.value_objects.composition import Composition
from src.domain.value_objects.calories import Calories
from src.domain.exceptions.domain_exception import PositionNotFound
from src.domain.uow.unit_of_work import IUnitOfWork

class UpdatePositionUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def execute(self, position_id: int, dto: PositionUpdateDTO) -> Position:
        position = await self.uow.position.get_by_id(position_id)
        if not position:
            raise PositionNotFound(f"Position with id {position_id} not found")

        if dto.title is not None:
            new_title = Title(dto.title)
            existing = await self.uow.position.get_by_title(new_title)
            if existing and existing.id != position_id:
                raise ValueError("Position with this title already exists")
            position.title = new_title

        if dto.price is not None:
            position.price = Price(amount=dto.price, currency="RUB")

        if dto.description is not None:
            position.description = Description(dto.description) if dto.description else None

        if dto.category is not None:
            position.category = Category(dto.category)

        if dto.composition is not None:
            position.composition = Composition(dto.composition) if dto.composition else None

        if dto.calories is not None:
            position.calories = Calories(dto.calories) if dto.calories is not None else None

        if dto.is_available is not None:
            position.is_avaliable = dto.is_available

        position = await self.uow.position.update(position)
        await self.uow.commit()
        return position