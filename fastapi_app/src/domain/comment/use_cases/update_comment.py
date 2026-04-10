from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comments import CommentRepository
from src.schemas.comment import CommentUpdate, Comment as CommentSchema
from src.core.exceptions import DomainError, NotFoundError, AuthorizationError, DatabaseError


class UpdateComment:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int, comment_data: CommentUpdate, current_user_id: int, is_superuser: bool) -> CommentSchema:
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
                    raise AuthorizationError("Вы можете редактировать только свои комментарии")
                
                update_data = comment_data.model_dump(exclude_unset=True)
                updated = self._repo.update(session, comment_id, **update_data)
                
            return CommentSchema.model_validate(updated)
        
        except (NotFoundError, AuthorizationError):
            raise
        except DatabaseError as e:
            raise DomainError(
                f"Ошибка базы данных при обновлении комментария ID={comment_id}",
                details={"comment_id": comment_id, "error": str(e)}
            )
        except Exception as e:
            raise DomainError(
                f"Неизвестная ошибка при обновлении комментария ID={comment_id}",
                details={"comment_id": comment_id, "error": str(e)}
            )