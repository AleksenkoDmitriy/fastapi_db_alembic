from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.api.depends import (
    users,
    user_by_id,
    user_by_login,
    create_user,
    update_user,
    delete_user,
    get_current_superuser,
    get_current_user
)
from src.domain.user.use_cases.get_users import GetUsers
from src.domain.user.use_cases.get_user_by_id import GetUserById
from src.domain.user.use_cases.get_user_by_login import GetUserByLogin
from src.domain.user.use_cases.create_user import CreateUser
from src.domain.user.use_cases.update_user import UpdateUser
from src.domain.user.use_cases.delete_user import DeleteUser
from src.core.exceptions.domain_exceptions import NotFoundError, DuplicateError, DomainError
from src.schemas.users import User, UserCreate, UserUpdate
from src.schemas.auth import TokenData

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[User])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    use_case: GetUsers = Depends(users),
    current_user: TokenData = Depends(get_current_superuser)
):
    """Только для суперпользователей"""
    try:
        return await use_case.execute(skip=skip, limit=limit)
    except DomainError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "details": e.details}
        )


@router.get("/me", response_model=User)
async def get_current_user_info(
    current_user: TokenData = Depends(get_current_user),
    use_case: GetUserById = Depends(user_by_id)
):
    """Информация о текущем пользователе"""
    try:
        user = await use_case.execute(current_user.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        return user
    except DomainError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "details": e.details}
        )


@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: int,
    use_case: GetUserById = Depends(user_by_id),
    current_user: TokenData = Depends(get_current_superuser)
):
    """Получить пользователя по ID. Только для суперпользователей"""
    try:
        user = await use_case.execute(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        return user
    except DomainError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "details": e.details}
        )


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    use_case: CreateUser = Depends(create_user)
):
    """Создать нового пользователя (открытый доступ)"""
    try:
        return await use_case.execute(user_data)
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


@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    use_case: UpdateUser = Depends(update_user),
    current_user: TokenData = Depends(get_current_superuser)
):
    """Обновить пользователя. Только для суперпользователей"""
    try:
        return await use_case.execute(user_id, user_data)
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


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    use_case: DeleteUser = Depends(delete_user),
    current_user: TokenData = Depends(get_current_superuser)
):
    """Удалить пользователя. Только для суперпользователей"""
    try:
        await use_case.execute(user_id)
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