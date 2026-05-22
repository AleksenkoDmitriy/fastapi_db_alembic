from typing import List
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.posts import PostRepository
from src.infrastructure.postgres.repositories.subscription import SubscriptionRepository
from src.schemas.posts import PostResponse
from src.core.exceptions.domain_exceptions import DomainError
from src.core.exceptions.infrastructure_exceptions import DatabaseError


class GetFeedUseCase:
    def __init__(self):
        self._database = database
        self._post_repo = PostRepository()
        self._subscription_repo = SubscriptionRepository()
    
    def execute(self, user_id: int, skip: int = 0, limit: int = 20) -> List[PostResponse]:
        try:
            with self._database.session() as session:
                # Получаем ID авторов, на которых подписан пользователь
                following_ids = self._subscription_repo.get_following(session, user_id)
                
                if not following_ids:
                    return []
                
                # Получаем посты этих авторов
                results = self._post_repo.get_posts_by_authors_with_likes_count(
                    session, following_ids, skip, limit
                )
                
                posts = []
                for post, likes_count in results:
                    post.likes_count = likes_count or 0
                    posts.append(PostResponse.model_validate(post))
                
                return posts
        
        except DatabaseError as e:
            raise DomainError(
                "Ошибка базы данных при получении ленты",
                details={"user_id": user_id, "error": str(e)}
            )