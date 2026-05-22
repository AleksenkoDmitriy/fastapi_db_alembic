from fastapi import APIRouter, Depends
from typing import List
from src.api.depends import (
    locations,
    location,
    create_location,
    update_location,
    delete_location,
    get_current_superuser
)
from src.domain.location.use_cases.get_locations import GetLocations
from src.domain.location.use_cases.get_location import GetLocation
from src.domain.location.use_cases.create_location import CreateLocation
from src.domain.location.use_cases.update_location import UpdateLocation
from src.domain.location.use_cases.delete_location import DeleteLocation
from src.schemas.location import Location, LocationCreate, LocationUpdate
from src.schemas.auth import TokenData

router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("/", response_model=List[Location])
async def get_locations(
    skip: int = 0,
    limit: int = 100,
    only_published: bool = True,
    use_case: GetLocations = Depends(locations)
):
    """Получить список локаций. Доступно всем."""
    return await use_case.execute(skip=skip, limit=limit, only_published=only_published)


@router.get("/{location_id}", response_model=Location)
async def get_location(
    location_id: int,
    use_case: GetLocation = Depends(location)
):
    """Получить локацию по ID. Доступно всем."""
    return await use_case.execute(location_id)


@router.post("/", response_model=Location, status_code=201)
async def create_location(
    location_data: LocationCreate,
    use_case: CreateLocation = Depends(create_location),
    current_user: TokenData = Depends(get_current_superuser)
):
    """Создать новую локацию. Только для суперпользователя."""
    return await use_case.execute(location_data)


@router.put("/{location_id}", response_model=Location)
async def update_location(
    location_id: int,
    location_data: LocationUpdate,
    use_case: UpdateLocation = Depends(update_location),
    current_user: TokenData = Depends(get_current_superuser)
):
    """Обновить локацию. Только для суперпользователя."""
    return await use_case.execute(location_id, location_data)


@router.delete("/{location_id}", status_code=204)
async def delete_location(
    location_id: int,
    use_case: DeleteLocation = Depends(delete_location),
    current_user: TokenData = Depends(get_current_superuser)
):
    """Удалить локацию. Только для суперпользователя."""
    await use_case.execute(location_id)
    return None