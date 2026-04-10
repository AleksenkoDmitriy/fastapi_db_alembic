from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.api.depends import (
    categories,
    category,
    category_by_slug,
    create_category,
    update_category,
    delete_category,
    get_current_superuser
)
from src.domain.category.use_cases.get_categories import GetCategories
from src.domain.category.use_cases.get_category import GetCategory
from src.domain.category.use_cases.get_category_by_slug import GetCategoryBySlug
from src.domain.category.use_cases.create_category import CreateCategory
from src.domain.category.use_cases.update_category import UpdateCategory
from src.domain.category.use_cases.delete_category import DeleteCategory
from src.core.exceptions.domain_exceptions import NotFoundError, DuplicateError, DomainError
from src.schemas.category import Category, CategoryCreate, CategoryUpdate
from src.schemas.auth import TokenData

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=List[Category])
async def get_categories(
    skip: int = 0,
    limit: int = 100,
    only_published: bool = True,
    use_case: GetCategories = Depends(categories)
):
    """Получить список категорий. Доступно всем."""
    try:
        return await use_case.execute(skip=skip, limit=limit, only_published=only_published)
    except DomainError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "details": e.details}
        )


@router.get("/{category_id}", response_model=Category)
async def get_category(
    category_id: int,
    use_case: GetCategory = Depends(category)
):
    """Получить категорию по ID. Доступно всем."""
    try:
        category_obj = await use_case.execute(category_id)
        if not category_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Категория не найдена"
            )
        return category_obj
    except DomainError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "details": e.details}
        )


@router.get("/slug/{slug}", response_model=Category)
async def get_category_by_slug(
    slug: str,
    use_case: GetCategoryBySlug = Depends(category_by_slug)
):
    """Получить категорию по slug. Доступно всем."""
    try:
        category_obj = await use_case.execute(slug)
        if not category_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Категория не найдена"
            )
        return category_obj
    except DomainError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "details": e.details}
        )


@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    use_case: CreateCategory = Depends(create_category),
    current_user: TokenData = Depends(get_current_superuser)
):
    """Создать новую категорию. Только для суперпользователя."""
    try:
        return await use_case.execute(category_data)
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


@router.put("/{category_id}", response_model=Category)
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    use_case: UpdateCategory = Depends(update_category),
    current_user: TokenData = Depends(get_current_superuser)
):
    """Обновить категорию. Только для суперпользователя."""
    try:
        return await use_case.execute(category_id, category_data)
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


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    use_case: DeleteCategory = Depends(delete_category),
    current_user: TokenData = Depends(get_current_superuser)
):
    """Удалить категорию. Только для суперпользователя."""
    try:
        await use_case.execute(category_id)
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