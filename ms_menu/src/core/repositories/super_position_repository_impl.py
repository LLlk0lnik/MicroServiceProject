from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from src.domain.repositories.super_position_repository import ISuperPositionRepository
from src.domain.entities.super_position import SuperPosition
from src.domain.entities.position import Position
from src.domain.value_objects.title import Title
from src.core.models.super_position_model import SuperPositionModel
from src.core.models.position_model import PositionModel
from src.core.mappers.super_position_mapper import to_domain, to_orm
from src.core.mappers.position_mapper import to_domain as position_to_domain
from src.core.models.associations import super_position_items

class SuperPositionRepository(ISuperPositionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, super_position_id: int) -> SuperPosition | None:
        result = await self.session.execute(
            select(SuperPositionModel)
            .where(SuperPositionModel.id == super_position_id)
            .options(selectinload(SuperPositionModel.positions))
        )
        model = result.scalar_one_or_none()
        return to_domain(model) if model else None

    async def get_by_title(self, title: Title) -> SuperPosition | None:
        result = await self.session.execute(
            select(SuperPositionModel)
            .where(SuperPositionModel.title == title.value)
            .options(selectinload(SuperPositionModel.positions))
        )
        model = result.scalar_one_or_none()
        return to_domain(model) if model else None

    async def get_all_available(self) -> list[SuperPosition]:
        result = await self.session.execute(
            select(SuperPositionModel)
            .where(SuperPositionModel.is_available == True)
            .options(selectinload(SuperPositionModel.positions))
        )
        models = result.scalars().all()
        return [to_domain(model) for model in models]

    async def add(self, super_position: SuperPosition) -> SuperPosition:
        model = to_orm(super_position)
        position_models = []
        for pos in super_position.positions:
            if pos.id:
                position_model = await self.session.get(PositionModel, pos.id)
                if position_model is None:
                    raise ValueError(f"Position with id {pos.id} not found")
                position_models.append(position_model)
            else:
                position_models.append(to_orm(pos))
        model.positions = position_models
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model, attribute_names=["positions"])
        super_position.id = model.id
        return to_domain(model)

    async def delete(self, super_position_id: int) -> None:
        super_position = await self.session.get(SuperPositionModel, super_position_id)
        if super_position:
            await self.session.delete(super_position)
            await self.session.flush()

    async def update(self, super_position: SuperPosition) -> SuperPosition:
        model = await self.session.get(SuperPositionModel, super_position.id)
        if not model:
            raise ValueError(f"SuperPosition with id {super_position.id} not found")

        model.title = super_position.title.value
        model.description = super_position.description.value if super_position.description else None
        model.is_available = super_position.is_available
        new_position_models = []
        for pos in super_position.positions:
            if pos.id:
                position_model = await self.session.get(PositionModel, pos.id)
                if position_model is None:
                    raise ValueError(f"Position with id {pos.id} not found")
                new_position_models.append(position_model)
            else:
                new_position_models.append(to_orm(pos))
        model.positions = new_position_models
        await self.session.flush()
        return await self.get_by_id(super_position.id)

    async def exists_by_title(self, title: Title) -> bool:
        result = await self.session.execute(
            select(SuperPositionModel)
            .where(SuperPositionModel.title == title.value)
            .limit(1)
        )
        return result.scalar_one_or_none() is not None

    async def get_positions_not_in_super(self, super_position_id: int) -> list[Position]:
        subquery = (select(super_position_items.c.position_id).where(super_position_items.c.super_position_id == super_position_id).subquery())
        result = await self.session.execute(
            select(PositionModel)
            .where(PositionModel.id.not_in(subquery))
        )
        models = result.scalars().all()
        return [position_to_domain(model) for model in models]

    async def get_position_not_in_super(self, super_position_id: int) -> list[Position]:
        return await self.get_positions_not_in_super(super_position_id)

    async def get_filtered(
        self,
        is_available: bool | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> tuple[list[SuperPosition], int]:
        query = select(SuperPositionModel).options(selectinload(SuperPositionModel.positions))
        if is_available is not None:
            query = query.where(SuperPositionModel.is_available == is_available)

        count_query = select(func.count()).select_from(query.subquery())
        total = await self.session.scalar(count_query)

        query = query.offset(offset).limit(limit)
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [to_domain(m) for m in models], total
