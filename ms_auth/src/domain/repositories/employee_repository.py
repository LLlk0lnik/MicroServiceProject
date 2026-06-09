from abc import ABC, abstractmethod
from src.domain.entities.employee import Employee
from src.domain.value_objects.phone_number import PhoneNumber


class IEmployeeRepository(ABC):
    @abstractmethod
    async def get_by_id(self, employee_id: int) -> Employee | None:
        pass

    @abstractmethod
    async def get_by_phone_number(self, phone_number: PhoneNumber) -> Employee | None:
        pass

    @abstractmethod
    async def add(self, employee: Employee) -> Employee:
        pass

    @abstractmethod
    async def update(self, employee: Employee) -> Employee:
        pass
