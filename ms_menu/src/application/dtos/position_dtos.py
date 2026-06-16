from pydantic import BaseModel, Field, field_validator
from decimal import Decimal
from src.domain.value_objects.category import Category


class PositionCreateDTO(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, pattern=r"^[a-zA-Zа-яА-ЯёЁ0-9\s\-]+$")
    price: Decimal = Field(..., ge=0, decimal_places=2)
    description: str | None = Field(None, max_length=500)
    category: Category
    composition: str | None = Field(None, max_length=1000)
    calories: int | None = Field(None, ge=0, le=10000)
    is_available: bool = True

    @field_validator("price")
    def validate_price(cls, v: Decimal) -> Decimal:
        if v > 999999.99:
            raise ValueError("Price too high")
        return v


class PositionUpdateDTO(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=100, pattern=r"^[a-zA-Zа-яА-ЯёЁ0-9\s\-]+$")
    price: Decimal | None = Field(None, ge=0, decimal_places=2)
    description: str | None = Field(None, max_length=500)
    category: Category | None = None
    composition: str | None = Field(None, max_length=1000)
    calories: int | None = Field(None, ge=0, le=10000)
    is_available: bool | None = None


class PositionResponseDTO(BaseModel):
    id: int
    title: str
    price: Decimal
    description: str | None
    category: str
    composition: str | None
    calories: int | None
    created_at: str
    is_available: bool


class PositionListResponseDTO(BaseModel):
    items: list[PositionResponseDTO]
    total: int
    limit: int
    offset: int