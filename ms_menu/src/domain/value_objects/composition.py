from dataclasses import dataclass
from ms_menu.src.domain.exceptions.domain_exception import InvalidComposition

@dataclass(frozen=True)
class Composition:
    value: str | None

    def __post_init__(self):
        if self.value is not None and len(self.value) > 1000:
            raise InvalidComposition("Composition cannot have more than 1000 characters")