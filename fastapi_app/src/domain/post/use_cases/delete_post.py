from pathlib import Path
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.posts import PostRepository
from src.core.exceptions import NotFoundError, AuthorizationError, DomainError, DatabaseError
from src.core.config import settings


class DeletePost:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int, current_user_id: int, is_superuser: bool) -> bool:
        try:
            with self._database.session() as session:
                existing = self._repo.get_by_id(session, post_id)
                if not existing:
                    raise NotFoundError(
                        entity_name="Пост",
                        field="id",
                        value=str(post_id)
                    )
                
                if existing.author_id != current_user_id and not is_superuser:
                    raise AuthorizationError("Вы можете удалять только свои посты")
                
                if existing.image:
                    try:
                        filename = Path(existing.image).name
                        image_path = Path(settings.UPLOAD_DIR) / filename
                        
                        if image_path.exists():
                            image_path.unlink()
                            print(f"Файл изображения удалён: {image_path} для поста {post_id}")
                    except Exception as e:
                        print(f"Предупреждение: Не удалось удалить файл изображения для поста {post_id}: {e}")
                
                deleted = self._repo.delete(session, post_id)
                return deleted
        
        except (NotFoundError, AuthorizationError):
            raise
        except DatabaseError as e:
            raise DomainError(
                f"Ошибка базы данных при удалении поста ID={post_id}",
                details={"post_id": post_id, "error": str(e)}
            )
        except Exception as e:
            raise DomainError(
                f"Неизвестная ошибка при удалении поста ID={post_id}",
                details={"post_id": post_id, "error": str(e)}
            )