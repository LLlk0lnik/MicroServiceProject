from src.domain.entities.OTP_code import OTP
from src.core.models.otp_models import OTPModel


def to_domain(model: OTPModel) -> OTP:
    return OTP(
        id=model.id,
        employee_id=model.employee_id,
        code=model.code,
        expires_at=model.expires_at,
        attempts=model.attempts,
        is_used=model.is_used,
        created_at=model.created_at,
    )


def to_orm(domain: OTP) -> OTPModel:
    return OTPModel(
        id=domain.id,
        employee_id=domain.employee_id,
        code=domain.code,
        expires_at=domain.expires_at,
        attempts=domain.attempts,
        is_used=domain.is_used,
        created_at=domain.created_at,
    )
