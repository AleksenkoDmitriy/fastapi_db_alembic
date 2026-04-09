from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.categories import CategoryRepository
from src.schemas.category import CategoryCreate, Category as CategorySchema
from src.core.exceptions import DomainError, DuplicateError, DatabaseError


class CreateCategory:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_data: CategoryCreate) -> CategorySchema:
        try:
            with self._database.session() as session:
                existing = self._repo.get_by_slug(session, category_data.slug)
                if existing:
                    raise DuplicateError(
                        entity_name="Категория",
                        field="slug",
                        value=category_data.slug
                    )
                
                category = self._repo.create(session, **category_data.model_dump())
                
            return CategorySchema.model_validate(category)
        
        except DuplicateError:
            raise
        except DatabaseError as e:
            raise DomainError(
                f"Ошибка базы данных при создании категории '{category_data.slug}'",
                details={"slug": category_data.slug, "error": str(e)}
            )
        except Exception as e:
            raise DomainError(
                f"Неизвестная ошибка при создании категории '{category_data.slug}'",
                details={"slug": category_data.slug, "error": str(e)}
            )