from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.users import UserRepository
from src.schemas.users import User as UserSchema
from src.core.exceptions import DomainError, DatabaseError, NotFoundError
from src.core.config import get_logger

logger = get_logger(__name__)

class GetUserByLogin:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, login: str) -> UserSchema:
        logger.info(f"Запрос пользователя по логину: {login}")

        try:
            with self._database.session() as session:
                user = self._repo.get_by_login(session, login)
                
                if not user:
                    logger.warning(f"Пользователь с логином '{login}' не найден")
                    raise NotFoundError(
                        entity_name="Пользователь",
                        field="login",
                        value=login
                    )
                
                user_data_dict = {
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
                }
                
            logger.info(f"Пользователь найден по логину: {login}")
            return UserSchema.model_validate(user_data_dict)
        
        except NotFoundError:
            raise
        except DatabaseError as e:
            logger.error(f"Ошибка БД при получении пользователя по логину '{login}', error={e}")
            raise DomainError(
                f"Ошибка базы данных при получении пользователя по логину '{login}'",
                details={"login": login, "error": str(e)}
            )
        except Exception as e:
            logger.exception(f"Неизвестная ошибка при получении пользователя по логину '{login}'")
            raise DomainError(
                f"Неизвестная ошибка при получении пользователя по логину '{login}'",
                details={"login": login, "error": str(e)}
            )