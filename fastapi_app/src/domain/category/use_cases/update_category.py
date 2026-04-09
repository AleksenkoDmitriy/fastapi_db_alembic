from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.categories import CategoryRepository
from src.schemas.category import CategoryUpdate, Category as CategorySchema
from src.core.exceptions import DomainError, NotFoundError, DuplicateError, DatabaseError


class UpdateCategory:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int, category_data: CategoryUpdate) -> CategorySchema:
        try:
            with self._database.session() as session:
                existing = self._repo.get_by_id(session, category_id)
                if not existing:
                    raise NotFoundError(
                        entity_name="Категория",
                        entity_id=category_id
                    )
                
                if category_data.slug and category_data.slug != existing.slug:
                    slug_exists = self._repo.get_by_slug(session, category_data.slug)
                    if slug_exists:
                        raise DuplicateError(
                            entity_name="Категория",
                            field="id",
                        value=str(category_id)
                    )
                
                update_data = category_data.model_dump(exclude_unset=True)
                category = self._repo.update(session, category_id, **update_data)
                
            return CategorySchema.model_validate(category)
        
        except (NotFoundError, DuplicateError):
            raise
        except DatabaseError as e:
            raise DomainError(
                f"Ошибка базы данных при обновлении категории ID={category_id}",
                details={"category_id": category_id, "error": str(e)}
            )
        except Exception as e:
            raise DomainError(
                f"Неизвестная ошибка при обновлении категории ID={category_id}",
                details={"category_id": category_id, "error": str(e)}
            )