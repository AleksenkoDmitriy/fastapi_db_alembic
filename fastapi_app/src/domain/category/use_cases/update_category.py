from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.categories import CategoryRepository
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
                        field="id",
                        value=str(category_id)
                    )
                
                if category_data.slug is not None and category_data.slug != existing.slug:
                    slug_exists = self._repo.get_by_slug(session, category_data.slug)
                    if slug_exists and slug_exists.id != category_id:
                        raise DuplicateError(
                            entity_name="Категория",
                            field="slug",
                            value=category_data.slug
                        )
                
                update_data = category_data.model_dump(exclude_unset=True)
                if update_data:
                    self._repo.update(session, category_id, **update_data)
                
                updated = self._repo.get_by_id(session, category_id)
                return CategorySchema.model_validate(updated)
        
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