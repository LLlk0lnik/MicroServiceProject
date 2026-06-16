from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from ms_menu.src.domain.repositories.super_position_repository import ISuperPositionRepository
from ms_menu.src.domain.entities.super_position import SuperPosition
from ms_menu.src.domain.value_objects.title import Title
from ms_menu.src.core.models.super_position_model import SuperPositionModel
from ms_menu.src.core.models.position_model import PositionModel
from ms_menu.src.core.mappers.super_position_mapper import to_domain, to_orm
from ms_menu.src.core.mappers.position_mapper import to_domain as position_to_domain
from ms_menu.src.core.models.position_model import super_position_items
from ms_menu.src.core.cache import async_cache

class SuperPositionRepository(ISuperPositionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    @async_cache(expire=60)
    async def get_by_id(self, super_position_id: int) -> SuperPosition | None:
        result = await self.session.execute(select(SuperPosition).where(SuperPosition.id == super_position_id).options(selectinload(SuperPositionModel.position)))
        model = result.scalar_one_or_none()
        return to_domain(model) if model else None

    async def get_by_title(self, title: Title) -> SuperPosition | None:
        result = await self.session.execute(select(SuperPosition).where(SuperPosition.title == title).options(selectinload(SuperPositionModel.position)))
        model = result.scalar_one_or_none()
        return to_domain(model) if model else None

    async def get_all_available(self) -> list[SuperPosition]:
        result = await self.session.execute(select(SuperPosition).where(SuperPosition.available == True).options(selectinload(SuperPositionModel.position)))
        models = result.scalars().all()
        return [to_domain(model) for model in models]

    async def add(self, super_position: SuperPosition) -> SuperPosition:
        model = to_orm(super_position)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model, attribute_name=["position"])
        super_position.id = model.id
        return super_position

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
                new_position_models.append(PositionModel(id=pos.id))
            else:
                new_position_models.append(to_orm(pos))
        model.positions = new_position_models
        await self.session.flush()
        return await self.get_by_id(super_position.id)


    async def get_position_not_in_super(self, super_position_id: int) -> list[SuperPosition]:
        subquery = (select(super_position_items.c.position_id).where(super_position_items.c.super_position_id == super_position_id).subquery())
        result = await self.session.execute(
            select(PositionModel)
            .where(PositionModel.id.not_in(subquery))
        )
        models = result.scalars().all()
        return [position_to_domain(model) for model in models]


