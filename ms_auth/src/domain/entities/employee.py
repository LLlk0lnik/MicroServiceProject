from dataclasses import dataclass
from datetime import datetime
from src.domain.value_objects.phone_number import PhoneNumber
from src.domain.value_objects.employee_role import EmployeeRole
from src.domain.value_objects.permission import Permission


@dataclass
class Employee:
    id: int | None
    phone_number: PhoneNumber
    name: str
    role: EmployeeRole
    is_active: bool
    created_at: datetime

    def active(self) -> None:
        self.is_active = True

    def deactive(self) -> None:
        self.is_active = False

    def change_role(self, new_role: EmployeeRole) -> None:
        self.role = new_role

    def has_permission(self, permission: Permission) -> bool:
        return permission in self.role.permissions()
