from decimal import Decimal
from dataclasses import dataclass
from src.domain.exceptions.domain_exception import InvalidPrice

@dataclass(frozen=True)
class Price:
    amount: Decimal
    currency: str = "RUB"

    def __post_init__(self):
        if self.amount < 0:
            raise InvalidPrice("Price cannot be negative")
        if self.amount.as_tuple().ecponent < -2:
            raise InvalidPrice("Price doesnt have more two characters after point")
        if self.currency not in ("RUB"):
            raise InvalidPrice("Not supported this currency")

    def __add__(self, other: 'Price') -> 'Price':
        if self.currency != other.currency:
            raise InvalidPrice("Price cannot have different currency")
        return Price(self.amount + other.amount, self.currency)