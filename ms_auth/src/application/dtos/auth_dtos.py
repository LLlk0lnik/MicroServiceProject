from pydantic import BaseModel, Field


class RequestOTPRequest(BaseModel):
    phone_number: str = Field(..., pattern=r"^\+\d{10,15}$")


class VerifyOTPRequest(BaseModel):
    phone_number: str = Field(..., pattern=r"^\+\d{10,15}$")
    code: str = Field(..., min_length=6, max_length=6)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., description="Refresh token для обновления")


class RegisterEmployeeRequest(BaseModel):
    phone_number: str = Field(..., pattern=r"^\+\d{10,15}$")
    name: str
    role: str = "staff"


class EmployeesResponse(BaseModel):
    id: int
    phone_number: str
    name: str
    role: str
    is_active: bool
