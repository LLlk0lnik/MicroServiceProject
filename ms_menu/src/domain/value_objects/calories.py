from dataclasses import dataclass
from src.domain.exceptions.domain_exception import InvalidCalories

@dataclass(frozen=True)
class Calories:
    value: int | None

    def __post_init__(self):
        if self.value is not None and self.value < 0 or self.value > 10000:
            raise InvalidCalories("invalid calories")

    def __add__(self, other: 'Calories') -> 'Calories':
        if self.value is None or other.value is None:
            return Calories(None)
        return Calories(self.value + other.value)
