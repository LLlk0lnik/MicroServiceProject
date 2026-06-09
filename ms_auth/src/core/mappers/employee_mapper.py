from src.domain.entities.employee import Employee
from src.domain.value_objects.phone_number import PhoneNumber
from src.domain.value_objects.employee_role import EmployeeRole
from src.core.models.employee_model import EmployeeModel


def to_domain(model: EmployeeModel) -> Employee:
    return Employee(
        id=model.id,
        phone_number=PhoneNumber(model.phone_number),
        name=model.name,
        role=EmployeeRole(model.role),
        is_active=model.is_active,
        created_at=model.created_at,
    )


def to_orm(domain: Employee) -> EmployeeModel:
    return EmployeeModel(
        id=domain.id,
        phone_number=domain.phone_number.value,
        name=domain.name,
        role=domain.role.value,
        is_active=domain.is_active,
        created_at=domain.created_at,
    )
