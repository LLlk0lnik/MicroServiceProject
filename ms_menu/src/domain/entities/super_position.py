from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from src.domain.value_objects.title import Title
from src.domain.value_objects.description import Description
from src.domain.value_objects.price import Price
from src.domain.value_objects.calories import Calories
from src.domain.entities.position import Position
from src.domain.exceptions.domain_exception import InvalidSuperPosition

@dataclass
class SuperPosition:
    id: int | None
    title: Title
    created_at: datetime
    description: Description | None = None
    positions: List[Position] = field(default_factory=list)
    is_available: bool = True

    def __post_init__(self):
        if not seld.positions:
            raise InvalidSuperPosition("superposition must have at least one position")
        first_currency = self.positions[0].price.currency
        for p in self.positions[1:]:
            if p.price.currency != first_currency:
                raise InvalidSuperPosition("all positions must have one currency")

    @property
    def total_price(self) -> Price:
        if not self.positions:
            return Price(0, "RUB")
        total = self.positions[0].price
        for p in self.positions[1:]:
            total += p.price
        return total

    @property
    def total_calories(self) -> Calories | None:
        total = Calories(0)
        for p in self.positions:
            total += p.calories
        return total

    @property
    def composition_summary(self) -> str:
        return ", ".join(p.title for p in self.positions)

    def add_position(self, position: Position) -> None:
        if position.price.currency != self.positions[0].price.currency:
            raise InvalidSuperPosition("superposition must have one currency")
        self.positions.append(position)

    def remove_position(self, position_id: int) -> None:
        self.positions = [p for p in self.positions if p.id != position_id]
        if not self.positions:
            raise InvalidSuperPosition("superposition must have at least one position")

    def active(self) -> bool:
        self.is_avaliable = True

    def deactive(self) -> bool:
        self.is_avaliable = False