from typing import List
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.users import UserRepository
from src.schemas.users import User as UserSchema
from src.core.exceptions import DomainError, DatabaseError


class GetUsers:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[UserSchema]:
        try:
            with self._database.session() as session:
                users = self._repo.get_all(session, skip, limit)
                
            return [UserSchema.model_validate(u) for u in users]
        
        except DatabaseError as e:
            raise DomainError(
                "Ошибка базы данных при получении списка пользователей",
                details={"skip": skip, "limit": limit, "error": str(e)}
            )
        except Exception as e:
            raise DomainError(
                "Неизвестная ошибка при получении списка пользователей",
                details={"skip": skip, "limit": limit, "error": str(e)}
            )