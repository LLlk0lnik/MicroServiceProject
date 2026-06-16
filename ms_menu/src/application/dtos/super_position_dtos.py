from pydantic import BaseModel, Field
from decimal import Decimal
from ms_menu.src.application.dtos.position_dtos import PositionResponseDTO


class SuperPositionCreateDTO(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, pattern=r"^[a-zA-Zа-яА-ЯёЁ0-9\s\-]+$")
    description: str | None = Field(None, max_length=500)
    position_ids: list[int] = Field(..., min_items=1)


class SuperPositionUpdateDTO(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=100, pattern=r"^[a-zA-Zа-яА-ЯёЁ0-9\s\-]+$")
    description: str | None = Field(None, max_length=500)
    position_ids: list[int] | None = Field(None, min_items=1)
    is_available: bool | None = None


class SuperPositionResponseDTO(BaseModel):
    id: int
    title: str
    description: str | None
    positions: list[PositionResponseDTO]
    total_price: Decimal
    total_calories: int | None
    composition_summary: str
    created_at: str
    is_available: bool