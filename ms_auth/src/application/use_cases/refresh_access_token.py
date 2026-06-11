from datetime import datetime, timedelta
from src.domain.uow.unit_of_work import IUnitOfWork
from src.domain.entities.refresh_token import RefreshToken
from src.domain.exceptions.domain_exceptions import EmployeeNotFound
from src.core.security.jwt_manager import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)
from src.config import settings


class InvalidTokenException(Exception):
    pass


class RefreshAccessTokenUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def execute(self, refresh_token: str) -> dict:
        token_entity = await self.uow.refresh_token.get_by_token(refresh_token)
        if not token_entity or not token_entity.is_valid():
            raise InvalidTokenException()

        payload = decode_refresh_token(refresh_token)
        if not payload:
            raise InvalidTokenException()

        employee_id = int(payload.get("sub"))

        token_entity = await self.uow.refresh_token.get_by_token(refresh_token)

        if not token_entity or not token_entity.is_valid():
            raise InvalidTokenException()

        employee = await self.uow.employee.get_by_id(employee_id)

        if not employee or not employee.is_active:
            raise EmployeeNotFound()

        token_entity.revoke()
        await self.uow.refresh_token.update(token_entity)

        access_token_data = {
            "sub": str(employee.id),
            "phone_number": str(employee.phone_number),
            "role": employee.role.value,
        }
        new_access_token = create_access_token(data=access_token_data)

        new_refresh_token_jwt = create_refresh_token(employee.id)

        new_token_entity = RefreshToken(
            id=None,
            token=new_refresh_token_jwt,
            employee_id=employee.id,
            expires_at=datetime.now()
            + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            is_revoked=False,
            created_at=datetime.now(),
        )

        await self.uow.refresh_token.add(new_token_entity)

        await self.uow.commit()

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token_jwt,
            "token_type": "bearer",
        }
