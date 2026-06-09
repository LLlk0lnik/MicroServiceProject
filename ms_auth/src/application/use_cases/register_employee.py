from datetime import datetime
from src.domain.uow.unit_of_work import IUnitOfWork
from src.domain.entities.employee import Employee
from src.domain.value_objects.phone_number import PhoneNumber
from src.domain.value_objects.employee_role import EmployeeRole


class RegisterEmployeeUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def execute(self, phone_number: str, name: str, role: str) -> Employee:
        phone_number_vo = PhoneNumber(phone_number)

        existing = await self.uow.employee.get_by_phone_number(phone_number_vo)
        if existing:
            raise ValueError("Employee with this phone number already exists")

        employee = Employee(
            id=None,
            phone_number=phone_number_vo,
            name=name,
            role=EmployeeRole(role),
            is_active=True,
            created_at=datetime.now(),
        )

        employee = await self.uow.employee.add(employee)
        await self.uow.commit()
        return employee
