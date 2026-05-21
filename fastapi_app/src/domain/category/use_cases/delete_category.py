from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.categories import CategoryRepository
from src.infrastructure.postgres.repositories.posts import PostRepository
from src.core.exceptions import NotFoundError, DomainError, DatabaseError
from src.core.exceptions.infrastructure_exceptions import ForeignKeyViolationError


class DeleteCategory:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()
        self._post_repo = PostRepository()

    async def execute(self, category_id: int) -> bool:
        try:
            with self._database.session() as session:
                existing = self._repo.get_by_id(session, category_id)
                if not existing:
                    raise NotFoundError(
                        entity_name="Категория",
                        field="id",
                        value=str(category_id)
                    )
                
                deleted = self._repo.delete(session, category_id)
                return deleted
        
        except ForeignKeyViolationError as e:
            with self._database.session() as session:
                posts = self._post_repo.get_by_category(session, category_id)
                post_ids = [post.id for post in posts]
            
            raise DomainError(
                f"Невозможно удалить категорию. К ней привязаны посты: {post_ids}",
                details={
                    "category_id": category_id,
                    "posts_count": len(post_ids),
                    "post_ids": post_ids,
                    "db_error": e.message
                }
            )
        
        except NotFoundError:
            raise
        
        except DatabaseError as e:
            raise DomainError(
                f"Ошибка базы данных при удалении категории ID={category_id}",
                details={"category_id": category_id, "error": e.message}
            )
        
        except Exception as e:
            raise DomainError(
                f"Неизвестная ошибка при удалении категории ID={category_id}",
                details={"category_id": category_id, "error": str(e)}
            )