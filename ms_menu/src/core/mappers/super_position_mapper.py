from src.domain.entities.super_position import SuperPosition
from src.domain.entities.position import Position
from src.domain.value_objects.title import Title
from src.domain.value_objects.description import Description
from src.core.models.super_position_model import SuperPositionModel
from src.core.models.position_model import PositionModel
from src.core.mappers.position_mapper import to_domain as position_to_domain, to_orm as position_to_orm

def to_domain(model: SuperPositionModel) -> SuperPosition:
    positions = [position_to_domain(position) for position in model.positions] if model.positions else []
    return SuperPosition(
        id=model.id,
        title=Title(model.title),
        description=Description(model.description) if model.description else None,
        positions=positions,
        created_at=model.created_at,
        is_available=model.is_available,
    )

def to_orm(entity: SuperPosition) -> SuperPositionModel:
    position_model = []
    for position in entity.positions:
        if position.id is not None:
            position_model.append(PositionModel(id=position.id))
        else:
            position_model.append(position_to_orm(position))

    return SuperPositionModel(
        id=entity.id,
        title=entity.title.value,
        description=entity.description.value if entity.description else None,
        created_at=entity.created_at,
        is_available=entity.is_available,
        positions=position_model,
    )
