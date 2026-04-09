from typing import List, Optional
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.posts import PostRepository
from src.schemas.posts import PostListResponse
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
    ) -> List[PostListResponse]:
        try:
            with self._database.session() as session:
                posts = self._repo.get_published(session, skip, limit, category_id)
                
            return [PostListResponse.model_validate(p) for p in posts]
        
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