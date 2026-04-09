from typing import List
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.locations import LocationRepository
from src.schemas.location import Location as LocationSchema
from src.core.exceptions import DomainError, DatabaseError


class GetLocations:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(
        self, 
        skip: int = 0, 
        limit: int = 100,
        only_published: bool = True
    ) -> List[LocationSchema]:
        try:
            with self._database.session() as session:
                if only_published:
                    locations = self._repo.get_published(session, skip, limit)
                else:
                    locations = self._repo.get_all(session, skip, limit)
                
            return [LocationSchema.model_validate(l) for l in locations]
        
        except DatabaseError as e:
            raise DomainError(
                "Ошибка базы данных при получении списка локаций",
                details={"skip": skip, "limit": limit, "error": str(e)}
            )
        except Exception as e:
            raise DomainError(
                "Неизвестная ошибка при получении списка локаций",
                details={"skip": skip, "limit": limit, "error": str(e)}
            )