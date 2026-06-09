from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.domain.repositories.employee_repository import IEmployeeRepository
from src.domain.entities.employee import Employee
from src.domain.value_objects.phone_number import PhoneNumber
from src.core.models.employee_model import EmployeeModel
from src.core.mappers.employee_mapper import to_domain, to_orm
from src.core.cache import async_cache


class EmployeeRepository(IEmployeeRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    @async_cache(expire=60)
    async def get_by_id(self, employee_id: int) -> Employee | None:
        result = await self.session.execute(
            select(EmployeeModel).where(EmployeeModel.id == employee_id)
        )
        model = result.scalar_one_or_none()
        return to_domain(model) if model else None

    async def get_by_phone_number(self, phone_number: PhoneNumber) -> Employee | None:
        result = await self.session.execute(
            select(EmployeeModel).where(
                EmployeeModel.phone_number == phone_number.value
            )
        )
        model = result.scalar_one_or_none()
        return to_domain(model) if model else None

    async def add(self, employee: Employee) -> Employee:
        model = to_orm(employee)
        self.session.add(model)
        await self.session.flush()
        employee.id = model.id
        return employee

    async def update(self, employee: Employee) -> Employee:
        model = to_orm(employee)
        await self.session.merge(model)
        return employee
