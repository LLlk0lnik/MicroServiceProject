from sqlalchemy import String, Integer, Boolean, DateTime, func, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from ms_menu.src.core.session import Base
from decimal import Decimal
from datetime import datetime
from ms_menu.src.core.models.super_position_model import SuperPositionModel, super_position_items

class PositionModel(Base):
    __tablename__ = 'positions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    description: Mapped[str | None] = mapped_column(String)
    category: Mapped[str] = mapped_column(String, nullable=False)
    composition: Mapped[str | None] = mapped_column(String)
    calories: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)

    super_position: Mapped[list["SuperPositionModel"]] = relationship(
        secondary=super_position_items,
        back_populates="positions",
        lazy="selectin"
    )