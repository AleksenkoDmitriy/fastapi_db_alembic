import logging
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.users import UserRepository
from src.schemas.users import User as UserSchema
from src.resources.auth import verify_password
from src.core.exceptions.domain_exceptions import UserNotFoundByLoginException, WrongPasswordException, AuthenticationError
from src.core.exceptions.infrastructure_exceptions import DatabaseError
from src.core.exceptions import DomainError

logger = logging.getLogger(__name__)


class AuthenticateUserUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = UserRepository()

    async def execute(
        self,
        login: str,
        password: str,
    ) -> UserSchema:
        try:
            with self._database.session() as session:
                user = self._repo.get_by_username(session, login)
                
                if not user:
                    error = UserNotFoundByLoginException(login=login)
                    logger.error(error.get_detail())
                    raise error
                
                if not verify_password(plain_password=password, hashed_password=user.password):
                    error = WrongPasswordException()
                    logger.error(error.get_detail())
                    raise error
                
                if not user.is_active:
                    error = AuthenticationError("Учетная запись деактивирована")
                    logger.error(error.message)
                    raise error
                
                return UserSchema.model_validate(obj=user)
        
        except (UserNotFoundByLoginException, WrongPasswordException, AuthenticationError):
            raise
        except DatabaseError as e:
            raise DomainError(
                f"Ошибка базы данных при аутентификации пользователя '{login}'",
                details={"login": login, "error": str(e)}
            )
        except Exception as e:
            raise DomainError(
                f"Неизвестная ошибка при аутентификации пользователя '{login}'",
                details={"login": login, "error": str(e)}
            )