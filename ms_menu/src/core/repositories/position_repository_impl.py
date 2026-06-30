from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from src.domain.repositories.position_repository import IPositionRepository
from src.domain.entities.position import Position
from src.domain.value_objects.title import Title
from src.domain.value_objects.category import Category
from src.core.models.position_model import PositionModel
from src.core.mappers.position_mapper import to_domain, to_orm

class PositionRepository(IPositionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

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
        result = await self.session.execute(select(PositionModel).where(PositionModel.is_available == True))
        models = result.scalars().all()
        return [to_domain(model) for model in models]

    async def get_all_available(self) -> list[Position]:
        return await self.get_all_avaliable()

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
        merged_model = await self.session.merge(model)
        await self.session.flush()
        return to_domain(merged_model)

    async def exists_by_title(self, title: Title) -> bool:
        result = await self.session.execute(select(PositionModel).where(PositionModel.title == title.value).limit(1))
        return result.scalar_one_or_none() is not None

    async def get_filtered(
        self,
        category: Category | None = None,
        is_available: bool | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> tuple[list[Position], int]:
        query = select(PositionModel)
        if category is not None:
            query = query.where(PositionModel.category == category.value)
        if is_available is not None:
            query = query.where(PositionModel.is_available == is_available)

        count_query = select(func.count()).select_from(query.subquery())
        total = await self.session.scalar(count_query)

        query = query.offset(offset).limit(limit)
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [to_domain(m) for m in models], total
