from ms_menu.src.application.dtos.position_dtos import PositionCreateDTO
from ms_menu.src.domain.entities.position import Position
from ms_menu.src.domain.value_objects.title import Title
from ms_menu.src.domain.value_objects.price import Price
from ms_menu.src.domain.value_objects.description import Description
from ms_menu.src.domain.value_objects.category import Category
from ms_menu.src.domain.value_objects.composition import Composition
from ms_menu.src.domain.value_objects.calories import Calories
from ms_menu.src.domain.uow.unit_of_work import IUnitOfWork
from datetime import datetime

class CreatePositionUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def execute(self, dto: PositionCreateDTO) -> Position:
        title_vo = Title(dto.title)
        existing = await self.uow.position.exists_by_title(title_vo)
        if existing:
            raise ValueError("Position with this title already exists")

        price_vo = Price(amount=dto.price, currency="RUB")
        description_vo = Description(dto.description) if dto.description else None
        category_vo = Category(dto.category)
        composition_vo = Composition(dto.composition) if dto.composition else None
        calories_vo = Calories(dto.calories) if dto.calories is not None else None

        position = Position(
            id=None,
            title=title_vo,
            price=price_vo,
            description=description_vo,
            category=category_vo,
            composition=composition_vo,
            calories=calories_vo,
            created_at=datetime.now(),
            is_avaliable=dto.is_available,
        )

        position = await self.uow.position.add(position)
        await self.uow.commit()
        return position