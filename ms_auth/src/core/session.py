from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)
from src.config import settings
from datetime import datetime
from sqlalchemy import Integer, func
from typing import AsyncGenerator

DATABASE_URL = settings.db_url

engine = create_async_engine(url=DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession() as session:
        yield session


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
