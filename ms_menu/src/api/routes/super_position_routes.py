from fastapi import APIRouter, Depends, HTTPException, Query
from src.application.use_cases.create_super_position import CreateSuperPositionUseCase
from src.application.use_cases.update_super_position import UpdateSuperPositionUseCase
from src.application.use_cases.delete_super_position import DeleteSuperPositionUseCase
from src.application.use_cases.get_super_position_by_id import GetSuperPositionByIdUseCase
from src.application.use_cases.get_super_positions import GetSuperPositionsUseCase
from src.application.use_cases.get_positions_not_in_super import GetPositionsNotInSuperPositionUseCase
from src.application.dtos.super_position_dtos import (
    SuperPositionCreateDTO,
    SuperPositionUpdateDTO,
    SuperPositionResponseDTO,
)
from src.application.dtos.position_dtos import PositionResponseDTO
from src.domain.exceptions.domain_exception import PositionNotFound, InvalidSuperPosition
from src.api.dependencies import (
    get_create_super_position_use_case,
    get_update_super_position_use_case,
    get_delete_super_position_use_case,
    get_get_super_position_by_id_use_case,
    get_get_super_positions_use_case,
    get_get_positions_not_in_super_use_case,
)

router = APIRouter(prefix="/super-positions", tags=["super-positions"])

@router.post("/", response_model=SuperPositionResponseDTO, status_code=201)
async def create_super_position(
    dto: SuperPositionCreateDTO,
    use_case: CreateSuperPositionUseCase = Depends(get_create_super_position_use_case),
):
    try:
        super_pos = await use_case.execute(dto)
        return _to_super_position_response(super_pos)
    except (ValueError, PositionNotFound, InvalidSuperPosition) as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{super_position_id}", response_model=SuperPositionResponseDTO)
async def update_super_position(
    super_position_id: int,
    dto: SuperPositionUpdateDTO,
    use_case: UpdateSuperPositionUseCase = Depends(get_update_super_position_use_case),
):
    try:
        super_pos = await use_case.execute(super_position_id, dto)
        return _to_super_position_response(super_pos)
    except ValueError as e:
        raise HTTPException(status_code=404 if "not found" in str(e) else 400, detail=str(e))
    except (PositionNotFound, InvalidSuperPosition) as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{super_position_id}", status_code=204)
async def delete_super_position(
    super_position_id: int,
    use_case: DeleteSuperPositionUseCase = Depends(get_delete_super_position_use_case),
):
    await use_case.execute(super_position_id)
    return None

@router.get("/{super_position_id}", response_model=SuperPositionResponseDTO)
async def get_super_position_by_id(
    super_position_id: int,
    use_case: GetSuperPositionByIdUseCase = Depends(get_get_super_position_by_id_use_case),
):
    try:
        super_pos = await use_case.execute(super_position_id)
        return _to_super_position_response(super_pos)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/", response_model=list[SuperPositionResponseDTO])
async def get_super_positions(
    is_available: bool | None = Query(None, description="Filter by availability"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    use_case: GetSuperPositionsUseCase = Depends(get_get_super_positions_use_case),
):
    super_positions, total = await use_case.execute(
        is_available=is_available,
        limit=limit,
        offset=offset,
    )
    return [_to_super_position_response(sp) for sp in super_positions]

@router.get("/{super_position_id}/available-positions", response_model=list[PositionResponseDTO])
async def get_positions_not_in_super(
    super_position_id: int,
    use_case: GetPositionsNotInSuperPositionUseCase = Depends(get_get_positions_not_in_super_use_case),
):
    positions = await use_case.execute(super_position_id)
    return [
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

def _to_super_position_response(super_pos):
    from src.application.dtos.super_position_dtos import SuperPositionResponseDTO
    return SuperPositionResponseDTO(
        id=super_pos.id,
        title=super_pos.title.value,
        description=super_pos.description.value if super_pos.description else None,
        positions=[
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
            for p in super_pos.positions
        ],
        total_price=super_pos.total_price.amount,
        total_calories=super_pos.total_calories.value if super_pos.total_calories else None,
        composition_summary=super_pos.composition_summary,
        created_at=super_pos.created_at.isoformat(),
        is_available=super_pos.is_available,
    )