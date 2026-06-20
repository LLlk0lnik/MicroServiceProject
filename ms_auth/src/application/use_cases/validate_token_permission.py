from src.domain.uow.unit_of_work import IUnitOfWork
from src.core.security.jwt_manager import decode_access_token
from src.domain.value_objects.employee_role import EmployeeRole
from src.domain.value_objects.permission import Permission

class InvalidAccessTokenException(Exception):
    pass

class PermissionDeniedException(Exception):
    pass

class ValidateTokenPermissionUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def execute(self, jwt_token: str, required_permission: Permission) -> dict:
        payload = decode_access_token(jwt_token)
        if not payload:
            raise InvalidAccessTokenException()

        role_value = payload.get("role")
        if not role_value:
            raise InvalidAccessTokenException()

        try:
            role = EmployeeRole(role_value)
        except ValueError:
            raise InvalidAccessTokenException()

        if required_permission not in role.permissions():
            raise PermissionDeniedException()

        return {
            "employee_id": payload.get("sub"),
            "role": role.value,
            "permissions": required_permission.value,
        }