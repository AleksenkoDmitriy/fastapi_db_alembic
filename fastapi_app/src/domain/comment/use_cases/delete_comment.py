from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comments import CommentRepository
from src.core.exceptions import NotFoundError, AuthorizationError, DomainError, DatabaseError


class DeleteComment:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int, current_user_id: int, is_superuser: bool) -> bool:
        try:
            with self._database.session() as session:
                existing = self._repo.get_by_id(session, comment_id)
                if not existing:
                    raise NotFoundError(
                        entity_name="Комментарий",
                        field="id",
                        value=str(comment_id)
                    )
                
                if existing.author_id != current_user_id and not is_superuser:
                    raise AuthorizationError("Вы можете удалять только свои комментарии")
                
                deleted = self._repo.delete(session, comment_id)
                return deleted
        
        except (NotFoundError, AuthorizationError):
            raise
        except DatabaseError as e:
            raise DomainError(
                f"Ошибка базы данных при удалении комментария ID={comment_id}",
                details={"comment_id": comment_id, "error": str(e)}
            )
        except Exception as e:
            raise DomainError(
                f"Неизвестная ошибка при удалении комментария ID={comment_id}",
                details={"comment_id": comment_id, "error": str(e)}
            )