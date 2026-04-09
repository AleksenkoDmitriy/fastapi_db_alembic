from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.locations import LocationRepository
from src.schemas.location import Location as LocationSchema
from src.core.exceptions import DomainError, DatabaseError


class GetLocation:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> LocationSchema | None:
        try:
            with self._database.session() as session:
                location = self._repo.get_by_id(session, location_id)
                
            if location:
                return LocationSchema.model_validate(location)
            return None
        
        except DatabaseError as e:
            raise DomainError(
                f"Ошибка базы данных при получении локации ID={location_id}",
                details={"location_id": location_id, "error": str(e)}
            )
        except Exception as e:
            raise DomainError(
                f"Неизвестная ошибка при получении локации ID={location_id}",
                details={"location_id": location_id, "error": str(e)}
            )