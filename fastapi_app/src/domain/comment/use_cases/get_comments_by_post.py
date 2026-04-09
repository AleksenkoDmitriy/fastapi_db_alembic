from typing import List
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comments import CommentRepository
from src.infrastructure.sqlite.repositories.posts import PostRepository
from src.schemas.comment import Comment as CommentSchema
from src.core.exceptions import DomainError, NotFoundError, DatabaseError


class GetCommentsByPost:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()
        self._post_repo = PostRepository()

    async def execute(self, post_id: int) -> List[CommentSchema]:
        try:
            with self._database.session() as session:
                post = self._post_repo.get_by_id(session, post_id)
                if not post:
                    raise NotFoundError(
                        entity_name="Пост",
                        field="id",
                        value=str(post_id)
                    )
                
                comments = self._repo.get_by_post(session, post_id)
                
            return [CommentSchema.model_validate(c) for c in comments]
        
        except NotFoundError:
            raise
        except DatabaseError as e:
            raise DomainError(
                f"Ошибка базы данных при получении комментариев поста ID={post_id}",
                details={"post_id": post_id, "error": str(e)}
            )
        except Exception as e:
            raise DomainError(
                f"Неизвестная ошибка при получении комментариев поста ID={post_id}",
                details={"post_id": post_id, "error": str(e)}
            )