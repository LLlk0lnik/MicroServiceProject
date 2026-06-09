from src.domain.uow.unit_of_work import IUnitOfWork
from src.core.security.jwt_manager import decode_refresh_token


class LogoutUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def execute(self, refresh_token: str) -> None:
        payload = decode_refresh_token(refresh_token)
        if not payload:
            return

        token_entity = await self.uow.refresh_token.get_by_token(refresh_token)
        if token_entity and not token_entity.is_revoked:
            token_entity.revoke()
            await self.uow.refresh_token.update(token_entity)
            await self.uow.commit()
