from typing import List
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.users import UserRepository
from src.schemas.users import User as UserSchema
from src.core.exceptions import DomainError, DatabaseError
from src.core.config import get_logger

logger = get_logger(__name__)

class GetUsers:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[UserSchema]:
        logger.info(f"Запрос списка пользователей: skip={skip}, limit={limit}")

        try:
            with self._database.session() as session:
                users = self._repo.get_all(session, skip, limit)
                
                users_data = []
                for user in users:
                    users_data.append({
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "is_superuser": user.is_superuser,
                        "is_staff": user.is_staff,
                        "is_active": user.is_active,
                        "last_login": user.last_login,
                        "date_joined": user.date_joined,
                    })
                
            logger.info(f"Получено {len(users_data)} пользователей")
            return [UserSchema.model_validate(u) for u in users_data]
        
        except DatabaseError as e:
            logger.error(f"Ошибка БД при получении списка пользователей, error={e}")
            raise DomainError(
                "Ошибка базы данных при получении списка пользователей",
                details={"skip": skip, "limit": limit, "error": str(e)}
            )
        except Exception as e:
            logger.exception(f"Неизвестная ошибка при получении списка пользователей")
            raise DomainError(
                "Неизвестная ошибка при получении списка пользователей",
                details={"skip": skip, "limit": limit, "error": str(e)}
            )