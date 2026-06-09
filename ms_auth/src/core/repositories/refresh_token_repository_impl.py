from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from datetime import datetime
from src.domain.repositories.refresh_token_repository import IRefreshTokenRepository
from src.domain.entities.refresh_token import RefreshToken
from src.core.models.refresh_token_model import RefreshTokenModel
from src.core.mappers.refresh_token_mapper import to_domain, to_orm


class RefreshTokenRepository(IRefreshTokenRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, token: RefreshToken) -> RefreshToken:
        model = to_orm(token)
        self.session.add(model)
        await self.session.flush()
        token.id = model.id
        return token

    async def get_by_token(self, token_value: str) -> RefreshToken | None:
        result = await self.session.execute(
            select(RefreshTokenModel).where(RefreshTokenModel.token == token_value)
        )
        model = result.scalar_one_or_none()
        return to_domain(model) if model else None

    async def update(self, token: RefreshToken) -> RefreshToken:
        model = to_orm(token)
        await self.session.merge(model)
        return token

    async def delete_expired(self) -> None:
        await self.session.execute(
            delete(RefreshTokenModel).where(
                RefreshTokenModel.expires_at < datetime.now()
            )
        )
