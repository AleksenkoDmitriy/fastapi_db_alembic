from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comments import CommentRepository
from src.core.exceptions import NotFoundError, DomainError, DatabaseError


class DeleteComment:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> bool:
        try:
            with self._database.session() as session:
                existing = self._repo.get_by_id(session, comment_id)
                if not existing:
                    raise NotFoundError(
                        entity_name="Комментарий",
                        field="id",
                        value=str(comment_id)
                    )
                
                deleted = self._repo.delete(session, comment_id)
                return deleted
        
        except NotFoundError:
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