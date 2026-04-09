from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.users import UserRepository
from src.infrastructure.sqlite.models.post import Post
from src.core.exceptions import NotFoundError, DomainError, DatabaseError


class DeleteUser:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> bool:
        try:
            with self._database.session() as session:
                existing = self._repo.get_by_id(session, user_id)
                if not existing:
                    raise NotFoundError(
                        entity_name="Пользователь",
                        field="id",
                        value=str(user_id)
                    )
                
                from sqlalchemy import delete
                stmt = delete(Post).where(Post.author_id == user_id)
                session.execute(stmt)
                
                deleted = self._repo.delete(session, user_id)
                return deleted
        
        except NotFoundError:
            raise
        except DatabaseError as e:
            raise DomainError(
                f"Ошибка базы данных при удалении пользователя ID={user_id}",
                details={"user_id": user_id, "error": str(e)}
            )
        except Exception as e:
            raise DomainError(
                f"Неизвестная ошибка при удалении пользователя ID={user_id}",
                details={"user_id": user_id, "error": str(e)}
            )