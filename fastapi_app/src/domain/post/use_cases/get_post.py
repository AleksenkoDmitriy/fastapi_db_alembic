from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.posts import PostRepository
from src.schemas.posts import PostResponse
from src.core.exceptions import DomainError, DatabaseError


class GetPost:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> PostResponse | None:
        try:
            with self._database.session() as session:
                result = self._repo.get_by_id_with_likes_count(session, post_id)
                
            if result:
                post, likes_count = result
                post.likes_count = likes_count or 0
                return PostResponse.model_validate(post)
            return None
        
        except DatabaseError as e:
            raise DomainError(
                f"Ошибка базы данных при получении поста ID={post_id}",
                details={"post_id": post_id, "error": str(e)}
            )
        except Exception as e:
            raise DomainError(
                f"Неизвестная ошибка при получении поста ID={post_id}",
                details={"post_id": post_id, "error": str(e)}
            )