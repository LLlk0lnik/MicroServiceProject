from abc import ABC, abstractmethod
from src.domain.entities.refresh_token import RefreshToken


class IRefreshTokenRepository(ABC):
    @abstractmethod
    async def add(self, token: RefreshToken) -> RefreshToken:
        pass

    @abstractmethod
    async def get_by_token(self, token_value: str) -> RefreshToken | None:
        pass

    @abstractmethod
    async def update(self, token: RefreshToken) -> RefreshToken:
        pass

    @abstractmethod
    async def delete_expired(self) -> None:
        pass
