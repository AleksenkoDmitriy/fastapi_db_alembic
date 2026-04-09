from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.users import UserRepository
from src.schemas.users import User as UserSchema
from src.core.exceptions import DomainError, DatabaseError


class GetUserById:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> UserSchema | None:
        try:
            with self._database.session() as session:
                 user = self._repo.get_by_id(session, user_id)
                
            if user:
                return UserSchema.model_validate(user)
            return None
        
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