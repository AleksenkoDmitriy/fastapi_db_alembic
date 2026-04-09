from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.users import UserRepository
from src.schemas.users import User as UserSchema
from src.core.exceptions import DomainError, DatabaseError


class GetUserByLogin:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, login: str) -> UserSchema | None:
        try:
            with self._database.session() as session:
                user = self._repo.get_by_login(session, login)
                
            if user:
                return UserSchema.model_validate(user)
            return None
        
        except DatabaseError as e:
            raise DomainError(
                f"Ошибка базы данных при получении пользователя по логину '{login}'",
                details={"login": login, "error": str(e)}
            )
        except Exception as e:
            raise DomainError(
                f"Неизвестная ошибка при получении пользователя по логину '{login}'",
                details={"login": login, "error": str(e)}
            )