from src.domain.entities.refresh_token import RefreshToken
from src.core.models.refresh_token_model import RefreshTokenModel


def to_domain(model: RefreshTokenModel) -> RefreshToken:
    return RefreshToken(
        id=model.id,
        token=model.token,
        employee_id=model.employee_id,
        expires_at=model.expires_at,
        is_revoked=model.is_revoked,
        created_at=model.created_at,
    )


def to_orm(domain: RefreshToken) -> RefreshTokenModel:
    return RefreshTokenModel(
        id=domain.id,
        token=domain.token,
        employee_id=domain.employee_id,
        expires_at=domain.expires_at,
        is_revoked=domain.is_revoked,
        created_at=domain.created_at,
    )
