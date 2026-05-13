from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.users import UserRepository
from src.schemas.users import User as UserSchema
from src.core.exceptions import DomainError, DatabaseError, NotFoundError


class GetUserById:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> UserSchema:
        try:
            with self._database.session() as session:
                user = self._repo.get_by_id(session, user_id)
                
                if not user:
                    raise NotFoundError(
                        entity_name="Пользователь",
                        field="id",
                        value=str(user_id)
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
                
            return UserSchema.model_validate(user_data_dict)
        
        except NotFoundError:
            raise
        except DatabaseError as e:
            raise DomainError(
                f"Ошибка базы данных при получении пользователя ID={user_id}",
                details={"user_id": user_id, "error": str(e)}
            )
        except Exception as e:
            raise DomainError(
                f"Неизвестная ошибка при получении пользователя ID={user_id}",
                details={"user_id": user_id, "error": str(e)}
            )