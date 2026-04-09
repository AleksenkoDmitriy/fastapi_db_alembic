from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.categories import CategoryRepository
from src.core.exceptions import NotFoundError, DomainError, DatabaseError


class DeleteCategory:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

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
        
        except NotFoundError:
            raise
        except DatabaseError as e:
            raise DomainError(
                f"Ошибка базы данных при удалении категории ID={category_id}",
                details={"category_id": category_id, "error": str(e)}
            )
        except Exception as e:
            raise DomainError(
                f"Неизвестная ошибка при удалении категории ID={category_id}",
                details={"category_id": category_id, "error": str(e)}
            )