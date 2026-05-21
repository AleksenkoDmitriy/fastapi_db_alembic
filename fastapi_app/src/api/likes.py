from fastapi import APIRouter, Depends, status
from src.api.depends import (
    get_current_user,
    get_add_like_use_case,
    get_remove_like_use_case,
    get_likes_count_use_case,
    get_check_user_like_use_case,
    get_user_likes_use_case
)
from src.domain.like.use_cases import (
    AddLikeUseCase,
    RemoveLikeUseCase,
    GetLikesCountUseCase,
    CheckUserLikeUseCase,
    GetUserLikesUseCase
)
from src.schemas.like import LikeResponse, LikeCreate
from src.schemas.auth import TokenData

router = APIRouter(prefix="/likes", tags=["likes"])

@router.post("/", response_model=LikeResponse, status_code=status.HTTP_201_CREATED)
def add_like(
    like_data: LikeCreate,
    current_user: TokenData = Depends(get_current_user),
    use_case: AddLikeUseCase = Depends(get_add_like_use_case)
):
    """Добавить лайк к посту"""
    like = use_case.execute(current_user.user_id, like_data.post_id)
    return like

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_like(
    post_id: int,
    current_user: TokenData = Depends(get_current_user),
    use_case: RemoveLikeUseCase = Depends(get_remove_like_use_case)
):
    """Удалить лайк с поста"""
    use_case.execute(current_user.user_id, post_id)
    return None

@router.get("/post/{post_id}/count")
def get_likes_count(
    post_id: int,
    use_case: GetLikesCountUseCase = Depends(get_likes_count_use_case)
):
    """Получить количество лайков поста"""
    count = use_case.execute(post_id)
    return {"post_id": post_id, "likes_count": count}

@router.get("/post/{post_id}/check")
def check_user_like(
    post_id: int,
    current_user: TokenData = Depends(get_current_user),
    use_case: CheckUserLikeUseCase = Depends(get_check_user_like_use_case)
):
    """Проверить, лайкнул ли пользователь пост"""
    liked = use_case.execute(current_user.user_id, post_id)
    return {"post_id": post_id, "liked": liked}

@router.get("/my-likes")
def get_my_likes(
    current_user: TokenData = Depends(get_current_user),
    use_case: GetUserLikesUseCase = Depends(get_user_likes_use_case)
):
    """Получить все посты, которые лайкнул текущий пользователь"""
    post_ids = use_case.execute(current_user.user_id)
    return {"user_id": current_user.user_id, "liked_post_ids": post_ids}