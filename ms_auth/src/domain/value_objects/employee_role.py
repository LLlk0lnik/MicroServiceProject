from enum import Enum
from src.domain.value_objects.permission import Permission


class EmployeeRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    STAFF = "staff"
    CLIENT = "client"

    def permissions(self) -> set[Permission]:
        mapping = {
            EmployeeRole.ADMIN: {
                Permission.CREATE_ORDER,
                Permission.VIEW_ORDER,
                Permission.MANAGE_EMPLOYMENT,
            },
            EmployeeRole.MANAGER: {
                Permission.CREATE_ORDER,
                Permission.VIEW_ORDER,
            },
            EmployeeRole.STAFF: {Permission.VIEW_ORDER},
            EmployeeRole.CLIENT: set(),
        }
        return mapping.get(self, set())
