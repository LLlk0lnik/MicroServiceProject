from dataclasses import dataclass
from datetime import datetime
from ms_menu.src.domain.value_objects.title import Title
from ms_menu.src.domain.value_objects.price import Price
from ms_menu.src.domain.value_objects.description import Description
from ms_menu.src.domain.value_objects.composition import Composition
from ms_menu.src.domain.value_objects.category import Category
from ms_menu.src.domain.value_objects.calories import Calories

@dataclass
class Position:
    id: int | None
    title: Title
    price: Price
    description: Description | None
    category: Category
    composition: Composition | None
    calories: Calories | None
    created_at: datetime
    is_avaliable: bool = True

    def update_price(self, new_price: Price) -> None:
        self.price = new_price

    def update_description(self, new_description: Description) -> None:
        self.description = new_description

    def update_composition(self, new_composition: Composition) -> None:
        self.composition = new_composition

    def active(self) -> bool:
        self.is_avaliable = True

    def deactive(self) -> bool:
        self.is_avaliable = False

