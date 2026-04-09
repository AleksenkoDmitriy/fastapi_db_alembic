from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.locations import LocationRepository
from src.core.exceptions import NotFoundError, DomainError, DatabaseError


class DeleteLocation:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> bool:
        try:
            with self._database.session() as session:
                existing = self._repo.get_by_id(session, location_id)
                if not existing:
                    raise NotFoundError(
                        entity_name="Локация",
                        field="id",
                        value=str(location_id)
                    )
                
                deleted = self._repo.delete(session, location_id)
                return deleted
        
        except NotFoundError:
            raise
        except DatabaseError as e:
            raise DomainError(
                f"Ошибка базы данных при удалении локации ID={location_id}",
                details={"location_id": location_id, "error": str(e)}
            )
        except Exception as e:
            raise DomainError(
                f"Неизвестная ошибка при удалении локации ID={location_id}",
                details={"location_id": location_id, "error": str(e)}
            )