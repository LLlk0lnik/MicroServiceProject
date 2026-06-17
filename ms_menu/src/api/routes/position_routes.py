from fastapi import APIRouter, Depends, HTTPException, Query
from src.application.use_cases.create_position import CreatePositionUseCase
from src.application.use_cases.update_position import UpdatePositionUseCase
from src.application.use_cases.delete_position import DeletePositionUseCase
from src.application.use_cases.get_position_by_id import GetPositionByIdUseCase
from src.application.use_cases.get_positions import GetPositionsUseCase
from src.application.dtos.position_dtos import (
    PositionCreateDTO,
    PositionUpdateDTO,
    PositionResponseDTO,
    PositionListResponseDTO,
)
from src.domain.exceptions.domain_exception import PositionNotFound
from src.api.dependencies import (
    get_create_position_use_case,
    get_update_position_use_case,
    get_delete_position_use_case,
    get_get_position_by_id_use_case,
    get_get_positions_use_case,
)

router = APIRouter(prefix="/positions", tags=["positions"])

@router.post("/", response_model=PositionResponseDTO, status_code=201)
async def create_position(
    dto: PositionCreateDTO,
    use_case: CreatePositionUseCase = Depends(get_create_position_use_case),
):
    try:
        position = await use_case.execute(dto)
        return PositionResponseDTO(
            id=position.id,
            title=position.title.value,
            price=position.price.amount,
            description=position.description.value if position.description else None,
            category=position.category.value,
            composition=position.composition.value if position.composition else None,
            calories=position.calories.value if position.calories is not None else None,
            created_at=position.created_at.isoformat(),
            is_available=position.is_avaliable,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{position_id}", response_model=PositionResponseDTO)
async def update_position(
    position_id: int,
    dto: PositionUpdateDTO,
    use_case: UpdatePositionUseCase = Depends(get_update_position_use_case),
):
    try:
        position = await use_case.execute(position_id, dto)
        return PositionResponseDTO(
            id=position.id,
            title=position.title.value,
            price=position.price.amount,
            description=position.description.value if position.description else None,
            category=position.category.value,
            composition=position.composition.value if position.composition else None,
            calories=position.calories.value if position.calories is not None else None,
            created_at=position.created_at.isoformat(),
            is_available=position.is_avaliable,
        )
    except PositionNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{position_id}", status_code=204)
async def delete_position(
    position_id: int,
    use_case: DeletePositionUseCase = Depends(get_delete_position_use_case),
):
    await use_case.execute(position_id)
    return None

@router.get("/{position_id}", response_model=PositionResponseDTO)
async def get_position_by_id(
    position_id: int,
    use_case: GetPositionByIdUseCase = Depends(get_get_position_by_id_use_case),
):
    try:
        position = await use_case.execute(position_id)
        return PositionResponseDTO(
            id=position.id,
            title=position.title.value,
            price=position.price.amount,
            description=position.description.value if position.description else None,
            category=position.category.value,
            composition=position.composition.value if position.composition else None,
            calories=position.calories.value if position.calories is not None else None,
            created_at=position.created_at.isoformat(),
            is_available=position.is_avaliable,
        )
    except PositionNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/", response_model=PositionListResponseDTO)
async def get_positions(
    category: str | None = Query(None, description="Filter by category"),
    is_available: bool | None = Query(None, description="Filter by availability"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    use_case: GetPositionsUseCase = Depends(get_get_positions_use_case),
):
    positions, total = await use_case.execute(
        category=category,
        is_available=is_available,
        limit=limit,
        offset=offset,
    )
    items = [
        PositionResponseDTO(
            id=p.id,
            title=p.title.value,
            price=p.price.amount,
            description=p.description.value if p.description else None,
            category=p.category.value,
            composition=p.composition.value if p.composition else None,
            calories=p.calories.value if p.calories is not None else None,
            created_at=p.created_at.isoformat(),
            is_available=p.is_avaliable,
        )
        for p in positions
    ]
    return PositionListResponseDTO(
        items=items,
        total=total,
        limit=limit,
        offset=offset,
    )