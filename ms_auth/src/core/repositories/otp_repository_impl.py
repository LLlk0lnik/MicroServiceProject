from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from src.domain.repositories.otp_repository import IOTPRepository
from src.domain.entities.OTP_code import OTP
from src.core.models.otp_models import OTPModel
from src.core.mappers.otp_mapper import to_domain, to_orm


class OTPRepository(IOTPRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, otp: OTP) -> OTP:
        model = to_orm(otp)
        self.session.add(model)
        await self.session.flush()
        otp.id = model.id
        return otp

    async def get_last_unused_by_employee(self, employee_id: int) -> OTP | None:
        result = await self.session.execute(
            select(OTPModel)
            .where(OTPModel.employee_id == employee_id, OTPModel.is_used == False)
            .order_by(desc(OTPModel.created_at))
            .limit(1)
        )
        model = result.scalar_one_or_none()
        return to_domain(model) if model else None

    async def update(self, otp: OTP) -> OTP:
        model = to_orm(otp)
        await self.session.merge(model)
        return otp
