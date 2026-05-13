from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.users import UserRepository
from src.infrastructure.postgres.models.post import Post
from src.infrastructure.postgres.models.comment import Comment
from src.core.exceptions import NotFoundError, DomainError, DatabaseError
from src.core.config import get_logger

logger = get_logger(__name__)

class DeleteUser:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> bool:
        logger.info(f"Попытка удаления пользователя с id={user_id}")

        try:
            with self._database.session() as session:
                existing = self._repo.get_by_id(session, user_id)
                if not existing:
                    logger.warning(f"Пользователь с id={user_id} не найден для удаления")
                    raise NotFoundError(
                        entity_name="Пользователь",
                        field="id",
                        value=str(user_id)
                    )
                
                from sqlalchemy import delete
                stmt_comments = delete(Comment).where(Comment.author_id == user_id)
                result_comments = session.execute(stmt_comments)
                logger.info(f"Удалено комментариев пользователя id={user_id}: {result_comments.rowcount}")
                
                stmt_posts = delete(Post).where(Post.author_id == user_id)
                result_posts = session.execute(stmt_posts)
                logger.info(f"Удалено постов пользователя id={user_id}: {result_posts.rowcount}")
                
                deleted = self._repo.delete(session, user_id)
                
            logger.info(f"Пользователь с id={user_id} успешно удален")
            return deleted
        
        except NotFoundError:
            raise
        except DatabaseError as e:
            logger.error(f"Ошибка БД при удалении пользователя id={user_id}, error={e}")
            raise DomainError(
                f"Ошибка базы данных при удалении пользователя ID={user_id}",
                details={"user_id": user_id, "error": str(e)}
            )
        except Exception as e:
            logger.exception(f"Неизвестная ошибка при удалении пользователя id={user_id}")
            raise DomainError(
                f"Неизвестная ошибка при удалении пользователя ID={user_id}",
                details={"user_id": user_id, "error": str(e)}
            )