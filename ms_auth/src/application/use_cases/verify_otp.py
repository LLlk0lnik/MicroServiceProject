from datetime import datetime, timedelta
from src.domain.uow.unit_of_work import IUnitOfWork
from src.domain.value_objects.phone_number import PhoneNumber
from src.domain.exceptions.domain_exceptions import (
    EmployeeNotFound,
    OTPInvalidException,
    OTPExpiredException,
    OTPMaxAttemptsExceeded,
)
from src.domain.entities.refresh_token import RefreshToken
from src.core.security.jwt_manager import create_access_token, create_refresh_token
from src.config import settings


class VerifyOTPUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def execute(self, phone_number: str, code: str) -> dict:
        phone_number_vo = PhoneNumber(phone_number)

        employee = await self.uow.employee.get_by_phone_number(phone_number_vo)
        if not employee:
            raise EmployeeNotFound()

        otp = await self.uow.OTP_code.get_last_unused_by_employee(employee.id)
        if not otp:
            raise OTPInvalidException()

        try:
            is_valid = otp.verify(code)
        except (
            OTPExpiredException,
            OTPMaxAttemptsExceeded,
            OTPInvalidException,
        ) as e:
            await self.uow.OTP_code.update(otp)
            await self.uow.commit()
            raise e

        if not is_valid:
            await self.uow.OTP_code.update(otp)
            await self.uow.commit()
            raise OTPInvalidException()

        await self.uow.OTP_code.update(otp)

        access_token_data = {
            "sub": str(employee.id),
            "phone_number": str(employee.phone_number),
            "role": employee.role.value,
        }
        access_token = create_access_token(
            data=access_token_data,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )

        refresh_token_jwt = create_refresh_token(employee.id)

        refresh_token_entity = RefreshToken(
            id=None,
            token=refresh_token_jwt,
            employee_id=employee.id,
            expires_at=datetime.now()
            + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            is_revoked=False,
            created_at=datetime.now(),
        )

        await self.uow.refresh_token.add(refresh_token_entity)
        await self.uow.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token_jwt,
            "token_type": "bearer",
        }
