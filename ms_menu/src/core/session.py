from sqlalchemy.orm import DeclarativeBase, declarative_base
from sqlalchemy.ext.asyncio import (
AsyncAttrs,
async_sessionmaker,
create_async_engine,
AsyncSession,
)

from src.config import settings
from typing import AsyncGenerator

DATABASE_URL = settings.db_url

engine = create_async_engine(url=DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession() as session:
        yield session

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    __table_args__ = {'schema': 'menu'}