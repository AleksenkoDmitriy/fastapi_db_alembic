from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.locations import LocationRepository
from src.schemas.location import LocationUpdate, Location as LocationSchema
from src.core.exceptions import DomainError, NotFoundError, DuplicateError, DatabaseError


class UpdateLocation:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int, location_data: LocationUpdate) -> LocationSchema:
        try:
            with self._database.session() as session:
                existing = self._repo.get_by_id(session, location_id)
                if not existing:
                    raise NotFoundError(
                        entity_name="Локация",
                        field="id",
                        value=str(location_id)
                    )
                
                if location_data.name and location_data.name != existing.name:
                    name_exists = self._repo.get_by_name(session, location_data.name)
                    if name_exists:
                        raise DuplicateError(
                            entity_name="Локация",
                            field="name",
                            value=location_data.name
                        )
                
                update_data = location_data.model_dump(exclude_unset=True)
                location = self._repo.update(session, location_id, **update_data)
                
            return LocationSchema.model_validate(location)
        
        except (NotFoundError, DuplicateError):
            raise
        except DatabaseError as e:
            raise DomainError(
                f"Ошибка базы данных при обновлении локации ID={location_id}",
                details={"location_id": location_id, "error": str(e)}
            )
        except Exception as e:
            raise DomainError(
                f"Неизвестная ошибка при обновлении локации ID={location_id}",
                details={"location_id": location_id, "error": str(e)}
            )