from typing import List, Optional
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.posts import PostRepository
from src.schemas.posts import PostResponse
from src.core.exceptions import DomainError, DatabaseError


class GetPosts:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(
        self,
        skip: int = 0,
        limit: int = 10,
        category_id: Optional[int] = None
    ) -> List[PostResponse]:
        try:
            with self._database.session() as session:
                results = self._repo.get_published_with_likes_count(
                    session, skip, limit, category_id
                )
                
            posts = []
            for post, likes_count in results:
                post.likes_count = likes_count or 0
                posts.append(PostResponse.model_validate(post))
            
            return posts
        
        except DatabaseError as e:
            raise DomainError(
                "Ошибка базы данных при получении списка постов",
                details={"skip": skip, "limit": limit, "category_id": category_id, "error": str(e)}
            )
        except Exception as e:
            raise DomainError(
                "Неизвестная ошибка при получении списка постов",
                details={"skip": skip, "limit": limit, "category_id": category_id, "error": str(e)}
            )