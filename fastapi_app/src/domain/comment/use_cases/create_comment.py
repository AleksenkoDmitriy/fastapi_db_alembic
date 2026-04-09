from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comments import CommentRepository
from src.infrastructure.sqlite.repositories.posts import PostRepository
from src.infrastructure.sqlite.repositories.users import UserRepository
from src.schemas.comment import CommentCreate, Comment as CommentSchema
from src.core.exceptions import DomainError, NotFoundError, DatabaseError


class CreateComment:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()
        self._post_repo = PostRepository()
        self._user_repo = UserRepository()

    async def execute(self, comment_data: CommentCreate) -> CommentSchema:
        try:
            with self._database.session() as session:
                post = self._post_repo.get_by_id(session, comment_data.post_id)
                if not post:
                    raise NotFoundError(
                        entity_name="Пост",
                        field="id",
                        value=str(comment_data.post_id)
                    )
                
                author = self._user_repo.get_by_id(session, comment_data.author_id)
                if not author:
                    raise NotFoundError(
                        entity_name="Автор",
                        field="id",
                        value=str(comment_data.author_id)
                    )
                
                comment = self._repo.create(session, **comment_data.model_dump())
                
            return CommentSchema.model_validate(comment)
        
        except NotFoundError:
            raise
        except DatabaseError as e:
            raise DomainError(
                f"Ошибка базы данных при создании комментария к посту ID={comment_data.post_id}",
                details={"post_id": comment_data.post_id, "error": str(e)}
            )
        except Exception as e:
            raise DomainError(
                f"Неизвестная ошибка при создании комментария",
                details={"post_id": comment_data.post_id, "error": str(e)}
            )