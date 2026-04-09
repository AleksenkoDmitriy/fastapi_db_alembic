from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.categories import CategoryRepository
from src.schemas.category import Category as CategorySchema
from src.core.exceptions import DomainError, NotFoundError, DatabaseError


class GetCategory:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> CategorySchema:
        try:
            with self._database.session() as session:
                category = self._repo.get_by_id(session, category_id)
                if not category:
                    raise NotFoundError(
                        entity_name="Категория",
                        field="id",
                        value=str(category_id)
                    )
                
            return CategorySchema.model_validate(category)
        
        except NotFoundError:
            raise
        except DatabaseError as e:
            raise DomainError(
                f"Ошибка базы данных при получении категории ID={category_id}",
                details={"category_id": category_id, "error": str(e)}
            )
        except Exception as e:
            raise DomainError(
                f"Неизвестная ошибка при получении категории ID={category_id}",
                details={"category_id": category_id, "error": str(e)}
            )