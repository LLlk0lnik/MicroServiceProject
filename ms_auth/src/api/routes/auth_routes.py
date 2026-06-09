from fastapi import APIRouter, Depends, HTTPException, status, Response
from src.application.use_cases.request_otp import RequestOtpUseCase
from src.application.use_cases.verify_otp import VerifyOTPUseCase
from src.application.use_cases.register_employee import RegisterEmployeeUseCase
from src.application.use_cases.refresh_access_token import (
    RefreshAccessTokenUseCase,
    InvalidTokenException,
)
from src.application.use_cases.logout import LogoutUseCase
from src.application.dtos.auth_dtos import (
    RequestOTPRequest,
    VerifyOTPRequest,
    TokenResponse,
    RefreshTokenRequest,
    RegisterEmployeeRequest,
    EmployeesResponse,
)
from src.domain.exceptions.domain_exceptions import (
    EmployeeNotFound,
    EmployeeInactiveException,
    InvalidPhoneNumber,
    OTPInvalidException,
    OTPExpiredException,
    OTPMaxAttemptsExceeded,
)
from src.core.repositories.employee_repository_impl import EmployeeRepository
from src.api.dependencies import (
    get_verify_otp_use_case,
    get_request_otp_use_case,
    get_refresh_token_use_case,
    get_logout_use_case,
    get_register_employee_use_case,
)

router = APIRouter()


@router.post("/register", response_model=EmployeesResponse, status_code=201)
async def register_employee(
    request: RegisterEmployeeRequest,
    use_case: RegisterEmployeeUseCase = Depends(get_register_employee_use_case),
):
    try:
        employee = await use_case.execute(
            request.phone_number, request.name, request.role
        )
        return EmployeesResponse(
            id=employee.id,
            phone_number=str(employee.phone_number),
            name=employee.name,
            role=employee.role.value,
            is_active=employee.is_active,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/request_otp", status_code=202)
async def request_otp(
    request: RequestOTPRequest,
    use_case: RequestOtpUseCase = Depends(get_request_otp_use_case),
):
    try:
        await use_case.execute(request.phone_number)
        return {"message": "OTP sent successfully"}
    except (EmployeeNotFound, EmployeeInactiveException) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidPhoneNumber as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/verify_otp", response_model=TokenResponse)
async def verify_otp(
    request: VerifyOTPRequest,
    use_case: VerifyOTPUseCase = Depends(get_verify_otp_use_case),
):
    try:
        token_data = await use_case.execute(request.phone_number, request.code)
        return TokenResponse(
            access_token=token_data["access_token"],
            refresh_token=token_data["refresh_token"],
            token_type="bearer",
        )
    except (
        EmployeeNotFound,
        OTPInvalidException,
        OTPExpiredException,
        OTPMaxAttemptsExceeded,
    ) as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    use_case: RefreshAccessTokenUseCase = Depends(get_refresh_token_use_case),
):
    try:
        token_data = await use_case.execute(request.refresh_token)
        return TokenResponse(
            access_token=token_data["access_token"],
            refresh_token=token_data["refresh_token"],
            token_type="bearer",
        )
    except (InvalidTokenException, EmployeeNotFound) as e:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


@router.post("/logout", status_code=204)
async def logout(
    request: RefreshTokenRequest,
    use_case: LogoutUseCase = Depends(get_logout_use_case),
):
    await use_case.execute(request.refresh_token)
    return Response(status_code=204)
