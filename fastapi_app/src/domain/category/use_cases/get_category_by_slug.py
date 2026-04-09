from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.categories import CategoryRepository
from src.schemas.category import Category as CategorySchema
from src.core.exceptions import DomainError, NotFoundError, DatabaseError


class GetCategoryBySlug:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, slug: str) -> CategorySchema:
        try:
            with self._database.session() as session:
                category = self._repo.get_by_slug(session, slug)
                if not category:
                    raise NotFoundError(
                        entity_name="Категория",
                        field="slug",
                        value=slug
                    )
                
            return CategorySchema.model_validate(category)
        
        except NotFoundError:
            raise
        except DatabaseError as e:
            raise DomainError(
                f"Ошибка базы данных при получении категории по slug '{slug}'",
                details={"slug": slug, "error": str(e)}
            )
        except Exception as e:
            raise DomainError(
                f"Неизвестная ошибка при получении категории по slug '{slug}'",
                details={"slug": slug, "error": str(e)}
            )