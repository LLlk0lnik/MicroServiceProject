import re
from dataclasses import dataclass
from src.domain.exceptions.domain_exception import InvalidTitle

@dataclass(frozen=True)
class Title:
    value: str

    def __post_init__(self):
        if not (1 <= len(self.value) <= 100):
            raise InvalidTitle("Title len must be between 1 and 100")
        if not re.match(r'^[a-zA-Zа-яА-Я0-9\s\-–—]+$', self.value):
            raise InvalidTitle("Title have invalid characters")

    def __str__(self) -> str:
        return self.value