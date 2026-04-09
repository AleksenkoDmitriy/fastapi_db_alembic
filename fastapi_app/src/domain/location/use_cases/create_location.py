from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.locations import LocationRepository
from src.schemas.location import LocationCreate, Location as LocationSchema
from src.core.exceptions import DuplicateError, DomainError, DatabaseError


class CreateLocation:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_data: LocationCreate) -> LocationSchema:
        try:
            with self._database.session() as session:
                existing = self._repo.get_by_name(session, location_data.name)
                if existing:
                    raise DuplicateError(
                        entity_name="Локация",
                        field="name",
                        value=location_data.name
                    )
                
                location = self._repo.create(session, **location_data.model_dump())
                
            return LocationSchema.model_validate(location)
        
        except DuplicateError:
            raise
        except DatabaseError as e:
            raise DomainError(
                f"Ошибка базы данных при создании локации '{location_data.name}'",
                details={"name": location_data.name, "error": str(e)}
            )
        except Exception as e:
            raise DomainError(
                f"Неизвестная ошибка при создании локации '{location_data.name}'",
                details={"name": location_data.name, "error": str(e)}
            )