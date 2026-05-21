from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.categories import CategoryRepository
from src.infrastructure.postgres.repositories.posts import PostRepository
from src.core.exceptions.domain_exceptions import NotFoundError, BusinessRuleError
from src.core.exceptions.infrastructure_exceptions import DatabaseError, ForeignKeyViolationError


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
                
                posts_with_category = self._post_repo.get_by_category(session, category_id)
                if posts_with_category:
                    raise BusinessRuleError(
                        f"Невозможно удалить категорию. Существует {len(posts_with_category)} пост(ов), использующих эту категорию.",
                        details={
                            "category_id": category_id,
                            "posts_count": len(posts_with_category),
                            "post_ids": [p.id for p in posts_with_category[:10]]
                        }
                    )
                
                deleted = self._repo.delete(session, category_id)
                return deleted
        
        except (NotFoundError, BusinessRuleError):
            raise
        except ForeignKeyViolationError as e:
            raise BusinessRuleError(
                "Невозможно удалить категорию, так как она используется в постах",
                details={"category_id": category_id, "error": str(e)}
            )
        except DatabaseError as e:
            raise DatabaseError(
                f"Ошибка базы данных при удалении категории ID={category_id}",
                details={"category_id": category_id, "error": str(e)}
            )