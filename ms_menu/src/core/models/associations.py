from sqlalchemy import Column, Table, ForeignKey
from src.core.session import Base

super_position_items = Table(
    "super_position_items",
    Base.metadata,
    Column("super_position_id", ForeignKey("menu.super_positions.id"), primary_key=True),
    Column("position_id", ForeignKey("menu.positions.id"), primary_key=True),
)
