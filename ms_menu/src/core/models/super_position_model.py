from sqlalchemy import String, Integer, Boolean, DateTime, func, Column, Table, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from ms_menu.src.core.session import Base
from datetime import datetime
from ms_menu.src.core.models.position_model import PositionModel

super_position_items = Table(
    "super_position_items",
    Base.metadata,
    Column("super_position_id", ForeignKey("super_positions.id"), primary_key=True),
    Column("position_id", ForeignKey("positions.id"), primary_key=True),
)

class SuperPositionModel(Base):
    __tablename__ = 'super_positions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    description: Mapped[str | None] = mapped_column(String)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)

    position: Mapped[list["PositionModel"]] = relationship(
        secondary=super_position_items,
        back_populates="super_positions",
        lazy="dynamic"
    )