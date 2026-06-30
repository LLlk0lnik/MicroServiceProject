from decimal import Decimal
from src.domain.entities.position import Position
from src.domain.value_objects.title import Title
from src.domain.value_objects.price import Price
from src.domain.value_objects.category import Category
from src.domain.value_objects.description import Description
from src.domain.value_objects.composition import Composition
from src.domain.value_objects.calories import Calories
from src.core.models.position_model import PositionModel

def to_domain(model: PositionModel) -> Position:
    return Position(
        id=model.id,
        title=Title(model.title),
        price=Price(amount=Decimal(str(model.price)), currency="RUB"),
        description=Description(model.description) if model.description else None,
        category=Category(model.category),
        composition=Composition(model.composition) if model.composition else None,
        calories=Calories(model.calories) if model.calories is not None else None,
        created_at=model.created_at,
        is_avaliable=model.is_available,
    )

def to_orm(entity: Position) -> PositionModel:
    return PositionModel(
        id=entity.id,
        title=entity.title.value,
        price=entity.price.amount,
        description=entity.description.value if entity.description else None,
        category=entity.category.value,
        composition=entity.composition.value if entity.composition else None,
        calories=entity.calories.value if entity.calories is not None else None,
        created_at=entity.created_at,
        is_available=entity.is_avaliable,
    )
