import re
from dataclasses import dataclass
from src.domain.exceptions.domain_exceptions import InvalidPhoneNumber

@dataclass(frozen=True)
class PhoneNumber:
    value: str

    def __post_init__(self):
        if not re.match(r"^\+\d{10,15}$", self.value):
            raise InvalidPhoneNumber()

    def __str__(self) -> str:
        return self.value
