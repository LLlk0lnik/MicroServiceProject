from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.session import get_session
from src.core.uow.sqlalchemy_uow import SQLAlchemyUnitOfWork
from src.application.use_cases.create_position import CreatePositionUseCase
from src.application.use_cases.update_position import UpdatePositionUseCase
from src.application.use_cases.delete_position import DeletePositionUseCase
from src.application.use_cases.get_position_by_id import GetPositionByIdUseCase
from src.application.use_cases.get_positions import GetPositionsUseCase
from src.application.use_cases.create_super_position import CreateSuperPositionUseCase
from src.application.use_cases.update_super_position import UpdateSuperPositionUseCase
from src.application.use_cases.delete_super_position import DeleteSuperPositionUseCase
from src.application.use_cases.get_super_position_by_id import GetSuperPositionByIdUseCase
from src.application.use_cases.get_super_positions import GetSuperPositionsUseCase
from src.application.use_cases.get_positions_not_in_super import GetPositionsNotInSuperPositionUseCase


async def get_create_position_use_case(
    session: AsyncSession = Depends(get_session)
) -> CreatePositionUseCase:
    uow = SQLAlchemyUnitOfWork(session)
    return CreatePositionUseCase(uow)

async def get_update_position_use_case(
    session: AsyncSession = Depends(get_session)
) -> UpdatePositionUseCase:
    uow = SQLAlchemyUnitOfWork(session)
    return UpdatePositionUseCase(uow)

async def get_delete_position_use_case(
    session: AsyncSession = Depends(get_session)
) -> DeletePositionUseCase:
    uow = SQLAlchemyUnitOfWork(session)
    return DeletePositionUseCase(uow)

async def get_get_position_by_id_use_case(
    session: AsyncSession = Depends(get_session)
) -> GetPositionByIdUseCase:
    uow = SQLAlchemyUnitOfWork(session)
    return GetPositionByIdUseCase(uow)

async def get_get_positions_use_case(
    session: AsyncSession = Depends(get_session)
) -> GetPositionsUseCase:
    uow = SQLAlchemyUnitOfWork(session)
    return GetPositionsUseCase(uow)

async def get_create_super_position_use_case(
    session: AsyncSession = Depends(get_session)
) -> CreateSuperPositionUseCase:
    uow = SQLAlchemyUnitOfWork(session)
    return CreateSuperPositionUseCase(uow)

async def get_update_super_position_use_case(
    session: AsyncSession = Depends(get_session)
) -> UpdateSuperPositionUseCase:
    uow = SQLAlchemyUnitOfWork(session)
    return UpdateSuperPositionUseCase(uow)

async def get_delete_super_position_use_case(
    session: AsyncSession = Depends(get_session)
) -> DeleteSuperPositionUseCase:
    uow = SQLAlchemyUnitOfWork(session)
    return DeleteSuperPositionUseCase(uow)

async def get_get_super_position_by_id_use_case(
    session: AsyncSession = Depends(get_session)
) -> GetSuperPositionByIdUseCase:
    uow = SQLAlchemyUnitOfWork(session)
    return GetSuperPositionByIdUseCase(uow)

async def get_get_super_positions_use_case(
    session: AsyncSession = Depends(get_session)
) -> GetSuperPositionsUseCase:
    uow = SQLAlchemyUnitOfWork(session)
    return GetSuperPositionsUseCase(uow)

async def get_get_positions_not_in_super_use_case(
    session: AsyncSession = Depends(get_session)
) -> GetPositionsNotInSuperPositionUseCase:
    uow = SQLAlchemyUnitOfWork(session)
    return GetPositionsNotInSuperPositionUseCase(uow)