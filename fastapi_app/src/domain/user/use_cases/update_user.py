from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.users import UserRepository
from src.schemas.users import UserUpdate, User as UserSchema
from src.core.exceptions import DomainError, NotFoundError, DuplicateError, DatabaseError


class UpdateUser:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int, user_data: UserUpdate) -> UserSchema:
        try:
            with self._database.session() as session:
                existing = self._repo.get_by_id(session, user_id)
                if not existing:
                    raise NotFoundError(
                        entity_name="Пользователь",
                        field="id",
                        value=str(user_id)
                    )
                
                if user_data.username and user_data.username != existing.username:
                    username_exists = self._repo.get_by_login(session, user_data.username)
                    if username_exists:
                        raise DuplicateError(
                            entity_name="Пользователь",
                            field="username",
                            value=user_data.username
                        )
                
                if user_data.email and user_data.email != existing.email:
                    email_exists = self._repo.get_by_email(session, user_data.email)
                    if email_exists:
                        raise DuplicateError(
                            entity_name="Пользователь",
                            field="email",
                            value=user_data.email
                        )
                
                update_data = user_data.model_dump(exclude_unset=True)
                updated = self._repo.update(session, user_id, **update_data)
                
            return UserSchema.model_validate(updated)
        
        except (NotFoundError, DuplicateError):
            raise
        except DatabaseError as e:
            raise DomainError(
                f"Ошибка базы данных при обновлении пользователя ID={user_id}",
                details={"user_id": user_id, "error": str(e)}
            )
        except Exception as e:
            raise DomainError(
                f"Неизвестная ошибка при обновлении пользователя ID={user_id}",
                details={"user_id": user_id, "error": str(e)}
            )