import random

from src.core.tasks.sms_task import send_otp_code_task
from src.domain.uow.unit_of_work import IUnitOfWork
from src.domain.entities.OTP_code import OTP
from src.domain.value_objects.phone_number import PhoneNumber
from src.domain.exceptions.domain_exceptions import (
    EmployeeNotFound,
    EmployeeInactiveException,
)


class RequestOtpUseCase:
    def __init__(
        self,
        uow: IUnitOfWork,
    ):
        self.uow = uow

    async def execute(self, phone_number: str) -> None:
        phone_number_vo = PhoneNumber(phone_number)

        employee = await self.uow.employee.get_by_phone_number(phone_number_vo)
        if not employee:
            raise EmployeeNotFound()
        if not employee.is_active:
            raise EmployeeInactiveException()

        code_value = f"{random.randint(0, 999999):06d}"
        otp = OTP.create(employee_id=employee.id, code_value=code_value)

        await self.uow.otp.add(otp)
        send_otp_code_task.delay(str(phone_number_vo), code_value)
        await self.uow.commit()
