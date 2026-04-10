from fastapi import APIRouter, Depends, HTTPException, status
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
from src.core.exceptions.domain_exceptions import NotFoundError, DuplicateError, DomainError
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
    try:
        return await use_case.execute(skip=skip, limit=limit, only_published=only_published)
    except DomainError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "details": e.details}
        )


@router.get("/{location_id}", response_model=Location)
async def get_location(
    location_id: int,
    use_case: GetLocation = Depends(location)
):
    """Получить локацию по ID. Доступно всем."""
    try:
        location = await use_case.execute(location_id)
        if not location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Локация не найдена"
            )
        return location
    except DomainError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "details": e.details}
        )


@router.post("/", response_model=Location, status_code=status.HTTP_201_CREATED)
async def create_location(
    location_data: LocationCreate,
    use_case: CreateLocation = Depends(create_location),
    current_user: TokenData = Depends(get_current_superuser)
):
    """Создать новую локацию. Только для суперпользователя."""
    try:
        return await use_case.execute(location_data)
    except DuplicateError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": e.message, "details": e.details}
        )
    except DomainError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "details": e.details}
        )


@router.put("/{location_id}", response_model=Location)
async def update_location(
    location_id: int,
    location_data: LocationUpdate,
    use_case: UpdateLocation = Depends(update_location),
    current_user: TokenData = Depends(get_current_superuser)
):
    """Обновить локацию. Только для суперпользователя."""
    try:
        return await use_case.execute(location_id, location_data)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "details": e.details}
        )
    except DuplicateError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": e.message, "details": e.details}
        )
    except DomainError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "details": e.details}
        )
    

@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_location(
    location_id: int,
    use_case: DeleteLocation = Depends(delete_location),
    current_user: TokenData = Depends(get_current_superuser)
):
    """Удалить локацию. Только для суперпользователя."""
    try:
        await use_case.execute(location_id)
        return None
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "details": e.details}
        )
    except DomainError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "details": e.details}
        )