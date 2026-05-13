from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.users import UserRepository
from src.schemas.users import UserCreate, User as UserSchema
from src.core.exceptions import DuplicateError, DomainError, DatabaseError
from src.resources.auth import get_password_hash
from src.core.config import get_logger

logger = get_logger(__name__)

class CreateUser:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_data: UserCreate) -> UserSchema:
        logger.info(f"Попытка создания пользователя с username: {user_data.username}, email: {user_data.email}")

        try:
            with self._database.session() as session:
                existing = self._repo.get_by_username(session, user_data.username)
                if existing:
                    logger.warning(f"Попытка создания дубликата пользователя по username: {user_data.username}")
                    raise DuplicateError(
                        entity_name="Пользователь",
                        field="username",
                        value=user_data.username
                    )
                
                existing_email = self._repo.get_by_email(session, user_data.email)
                if existing_email:
                    logger.warning(f"Попытка создания дубликата пользователя по email: {user_data.email}")
                    raise DuplicateError(
                        entity_name="Пользователь",
                        field="email",
                        value=user_data.email
                    )
                
                user_dict = user_data.model_dump()
                user_dict["password"] = get_password_hash(user_dict.pop("password"))
                
                user = self._repo.create(session, **user_dict)
                
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
                
            logger.info(f"Пользователь успешно создан: id={user.id}, username={user.username}")
            return UserSchema.model_validate(user_data_dict)
        
        except DuplicateError:
            raise
        except DatabaseError as e:
            logger.error(f"Ошибка БД при создании пользователя: {user_data.username}, error={e}")
            raise DomainError(
                f"Ошибка базы данных при создании пользователя '{user_data.username}'",
                details={"username": user_data.username, "error": str(e)}
            )
        except Exception as e:
            logger.exception(f"Неизвестная ошибка при создании пользователя: {user_data.username}")
            raise DomainError(
                f"Неизвестная ошибка при создании пользователя '{user_data.username}'",
                details={"username": user_data.username, "error": str(e)}
            )