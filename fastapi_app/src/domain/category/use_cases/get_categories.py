from typing import List
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.categories import CategoryRepository
from src.schemas.category import Category as CategorySchema
from src.core.exceptions import DomainError, DatabaseError


class GetCategories:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(
        self, 
        skip: int = 0, 
        limit: int = 100,
        only_published: bool = True
    ) -> List[CategorySchema]:
        try:
            with self._database.session() as session:
                if only_published:
                    categories = self._repo.get_published(session, skip, limit)
                else:
                    categories = self._repo.get_all(session, skip, limit)
                
            return [CategorySchema.model_validate(c) for c in categories]
        
        except DatabaseError as e:
            raise DomainError(
                "Ошибка базы данных при получении списка категорий",
                details={"skip": skip, "limit": limit, "error": str(e)}
            )
        except Exception as e:
            raise DomainError(
                "Неизвестная ошибка при получении списка категорий",
                details={"skip": skip, "limit": limit, "error": str(e)}
            )