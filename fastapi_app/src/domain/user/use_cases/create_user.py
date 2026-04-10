from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.users import UserRepository
from src.schemas.users import UserCreate, User as UserSchema
from src.core.exceptions import DuplicateError, DomainError, DatabaseError
from src.resources.auth import get_password_hash


class CreateUser:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_data: UserCreate) -> UserSchema:
        try:
            with self._database.session() as session:
                existing = self._repo.get_by_username(session, user_data.username)
                if existing:
                    raise DuplicateError(
                        entity_name="Пользователь",
                        field="username",
                        value=user_data.username
                    )
                
                existing_email = self._repo.get_by_email(session, user_data.email)
                if existing_email:
                    raise DuplicateError(
                        entity_name="Пользователь",
                        field="email",
                        value=user_data.email
                    )
                
                user_dict = user_data.model_dump()
                user_dict["password"] = get_password_hash(user_dict.pop("password"))
                
                user = self._repo.create(session, **user_dict)
                
            return UserSchema.model_validate(user)
        
        except DuplicateError:
            raise
        except DatabaseError as e:
            raise DomainError(
                f"Ошибка базы данных при создании пользователя '{user_data.username}'",
                details={"username": user_data.username, "error": str(e)}
            )
        except Exception as e:
            raise DomainError(
                f"Неизвестная ошибка при создании пользователя '{user_data.username}'",
                details={"username": user_data.username, "error": str(e)}
            )