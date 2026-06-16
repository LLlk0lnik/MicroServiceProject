from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ms_menu.src.domain.repositories.position_repository import IPositionRepository
from ms_menu.src.domain.entities.position import Position
from ms_menu.src.domain.value_objects.title import Title
from ms_menu.src.domain.value_objects.category import Category
from ms_menu.src.core.models.position_model import PositionModel
from ms_menu.src.core.mappers.position_mapper import to_domain, to_orm
from ms_menu.src.core.cache import async_cache

class PositionRepository(IPositionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    @async_cache(expire=60)
    async def get_by_id(self, position_id: int) -> Position | None:
        result = await self.session.execute(select(PositionModel).where(PositionModel.id == position_id))
        model = result.scalar_one_or_none()
        return to_domain(model) if model else None

    async def get_by_title(self, title: Title) -> Position | None:
        result = await self.session.execute(select(PositionModel).where(PositionModel.title == title.value))
        model = result.scalar_one_or_none()
        return to_domain(model) if model else None

    async def get_by_category(self, category: Category) -> list[Position]:
        result = await self.session.execute(select(PositionModel).where(PositionModel.category == category.value))
        models = result.scalars().all()
        return [to_domain(model) for model in models]

    async def get_all_avaliable(self) -> list[Position]:
        result = await self.session.execute(select(PositionModel).where(PositionModel.avaliable == True))
        models = result.scalars().all()
        return [to_domain(model) for model in models]

    async def add(self, position: Position) -> Position:
        model = to_orm(position)
        self.session.add(model)
        await self.session.flush()
        position.id = model.id
        return position

    async def delete(self, position_id: int) -> None:
        position = await self.session.get(PositionModel, position_id)
        if position:
            await self.session.delete(position)
            await self.session.flush()

    async def update(self, position: Position) -> Position:
        model = to_orm(position)
        merged_mmodel = await self.session.merge(model)
        await self.session.flush()
        return to_domain(merged_mmodel)

    async def exists_by_title(self, title: Title) -> bool:
        result = await self.session.execute(Select(PositionModel).where(PositionModel.title == title.value).limit(1))
        return result.scalar_one_or_none() is not None



