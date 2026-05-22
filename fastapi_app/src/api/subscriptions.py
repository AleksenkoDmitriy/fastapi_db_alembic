from fastapi import APIRouter, Depends
from typing import List
from src.api.depends import (
    get_current_user,
    get_follow_use_case,
    get_unfollow_use_case,
    get_feed_use_case,
    get_following_use_case,
    get_followers_use_case,
    get_stats_use_case
)
from src.schemas.subscription import FollowResponse, FollowingResponse, FollowersResponse, SubscriptionStats
from src.schemas.auth import TokenData
from src.schemas.posts import PostResponse

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


@router.post("/{author_id}", response_model=FollowResponse, status_code=201)
def follow_author(
    author_id: int,
    current_user: TokenData = Depends(get_current_user),
    use_case = Depends(get_follow_use_case)
):
    """Подписаться на автора"""
    return use_case.execute(current_user.user_id, author_id)


@router.delete("/{author_id}", status_code=204)
def unfollow_author(
    author_id: int,
    current_user: TokenData = Depends(get_current_user),
    use_case = Depends(get_unfollow_use_case)
):
    """Отписаться от автора"""
    use_case.execute(current_user.user_id, author_id)
    return None


@router.get("/feed", response_model=List[PostResponse])
def get_feed(
    skip: int = 0,
    limit: int = 20,
    current_user: TokenData = Depends(get_current_user),
    use_case = Depends(get_feed_use_case)
):
    """Получить ленту постов от подписанных авторов"""
    return use_case.execute(current_user.user_id, skip, limit)


@router.get("/following", response_model=List[FollowingResponse])
def get_following(
    skip: int = 0,
    limit: int = 50,
    current_user: TokenData = Depends(get_current_user),
    use_case = Depends(get_following_use_case)
):
    """Получить список авторов, на которых подписан пользователь"""
    return use_case.execute(current_user.user_id, skip, limit)


@router.get("/followers", response_model=List[FollowersResponse])
def get_followers(
    skip: int = 0,
    limit: int = 50,
    current_user: TokenData = Depends(get_current_user),
    use_case = Depends(get_followers_use_case)
):
    """Получить список подписчиков пользователя"""
    return use_case.execute(current_user.user_id, skip, limit)


@router.get("/stats/{user_id}", response_model=SubscriptionStats)
def get_subscription_stats(
    user_id: int,
    current_user: TokenData = Depends(get_current_user),
    use_case = Depends(get_stats_use_case)
):
    """Получить статистику подписок пользователя"""
    return use_case.execute(user_id, current_user.user_id)