from dataclasses import dataclass
from ms_menu.src.domain.exceptions.domain_exception import InvalidDescription
@dataclass(frozen=True)
class Description:
    value: str | None

    def __post_init__(self):
        if self.value is not None and len(self.value) > 300:
            raise InvalidDescription("Description cannot have more than 300 characters")