from sqlalchemy import String, Integer, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.session import Base
from datetime import datetime
from src.core.models.associations import super_position_items

class SuperPositionModel(Base):
    __tablename__ = 'super_positions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    description: Mapped[str | None] = mapped_column(String)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)

    positions: Mapped[list["PositionModel"]] = relationship(
        secondary=super_position_items,
        back_populates="super_positions",
        lazy="dynamic"
    )