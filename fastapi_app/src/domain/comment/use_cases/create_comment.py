from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.comments import CommentRepository
from src.infrastructure.postgres.repositories.posts import PostRepository
from src.schemas.comment import CommentCreate, Comment as CommentSchema
from src.core.exceptions import DomainError, NotFoundError, DatabaseError
from src.infrastructure.postgres.models.users import User


class CreateComment:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()
        self._post_repo = PostRepository()

    async def execute(self, comment_data: CommentCreate, author_id: int) -> CommentSchema:
        try:
            with self._database.session() as session:
                post = self._post_repo.get_by_id(session, comment_data.post_id)
                if not post:
                    raise NotFoundError(
                        entity_name="Пост",
                        field="id",
                        value=str(comment_data.post_id)
                    )
                
                comment_dict = comment_data.model_dump()
                comment_dict["author_id"] = author_id
                
                comment = self._repo.create(session, **comment_dict)
                
                session.refresh(comment)
                comment.author = session.get(User, author_id)
                
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