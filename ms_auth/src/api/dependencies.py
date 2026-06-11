from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.security.jwt_manager import decode_access_token
from src.domain.entities.employee import Employee
from src.application.use_cases.request_otp import RequestOtpUseCase
from src.application.use_cases.verify_otp import VerifyOTPUseCase
from src.application.use_cases.refresh_access_token import RefreshAccessTokenUseCase
from src.application.use_cases.logout import LogoutUseCase
from src.domain.value_objects.permission import Permission
from src.core.session import get_session
from src.core.uow.sqlalchemy_uow import SQLAlchemyUnitOfWork
from src.application.use_cases.register_employee import RegisterEmployeeUseCase

security = HTTPBearer()


def require_permission(permission: Permission):
    async def permission_checher(
        current_employee: Employee = Depends(get_current_employee),
    ) -> Employee:
        if not current_employee.has_permission(required_permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing permission: {required_permission.value}",
            )
        return current_employee

    return permission_checher


async def get_current_employee_payload(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )
    return payload


async def get_current_employee_id(
    payload: dict = Depends(get_current_employee_payload),
) -> int:
    employee_id = payload.get("sub")
    if not employee_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
        )
    return int(employee_id)


async def get_current_employee(
    employee_id: int = Depends(get_current_employee_id),
    session: AsyncSession = Depends(get_session),
) -> Employee:
    uow = SQLAlchemyUnitOfWork(session)
    employee = await uow.employee.get_by_id(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


async def get_verify_otp_use_case(
    session: AsyncSession = Depends(get_session),
) -> VerifyOTPUseCase:
    uow = SQLAlchemyUnitOfWork(session)
    return VerifyOTPUseCase(uow)


async def get_request_otp_use_case(
    session: AsyncSession = Depends(get_session),
) -> RequestOtpUseCase:
    uow = SQLAlchemyUnitOfWork(session)
    return RequestOtpUseCase(uow)


async def get_refresh_token_use_case(
    session: AsyncSession = Depends(get_session),
) -> RefreshAccessTokenUseCase:
    uow = SQLAlchemyUnitOfWork(session)
    return RefreshAccessTokenUseCase(uow)


async def get_logout_use_case(
    session: AsyncSession = Depends(get_session),
) -> LogoutUseCase:
    uow = SQLAlchemyUnitOfWork(session)
    return LogoutUseCase(uow)


async def get_register_employee_use_case(
    session: AsyncSession = Depends(get_session),
) -> RegisterEmployeeUseCase:
    uow = SQLAlchemyUnitOfWork(session)
    return RegisterEmployeeUseCase(uow)
