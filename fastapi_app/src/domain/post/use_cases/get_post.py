from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.posts import PostRepository
from src.schemas.posts import Post as PostSchema
from src.core.exceptions import DomainError, DatabaseError


class GetPost:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> PostSchema | None:
        try:
            with self._database.session() as session:
                post = self._repo.get_by_id_with_relations(session, post_id)
                
            if post:
                return PostSchema.model_validate(post)
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