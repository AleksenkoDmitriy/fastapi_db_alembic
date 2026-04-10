from fastapi import HTTPException, status


class CredentialsException(HTTPException):
    def __init__(self, detail: str = "Не удалось подтвердить учетные данные") -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class TokenExpiredException(HTTPException):
    def __init__(self, detail: str = "Срок действия токена истек") -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class InvalidTokenException(HTTPException):
    def __init__(self, detail: str = "Недействительный токен") -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class InsufficientPermissionsException(HTTPException):
    def __init__(self, detail: str = "Недостаточно прав") -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class UserNotFoundException(HTTPException):
    def __init__(self, detail: str = "Пользователь не найден") -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


class UserInactiveException(HTTPException):
    def __init__(self, detail: str = "Учетная запись пользователя неактивна") -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class InvalidPasswordException(HTTPException):
    def __init__(self, detail: str = "Неверный пароль") -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


def handle_domain_auth_error(exc):
    """Преобразование доменных ошибок аутентификации в HTTP исключения"""
    from src.core.exceptions.domain_exceptions import (
        UserNotFoundByLoginException,
        WrongPasswordException,
        AuthenticationError,
        TokenError,
        AuthorizationError
    )
    
    if isinstance(exc, UserNotFoundByLoginException):
        return UserNotFoundException(detail=exc.message)
    elif isinstance(exc, WrongPasswordException):
        return InvalidPasswordException(detail=exc.message)
    elif isinstance(exc, AuthenticationError):
        if "деактивирована" in exc.message or "inactive" in exc.message.lower():
            return UserInactiveException(detail=exc.message)
        return CredentialsException(detail=exc.message)
    elif isinstance(exc, TokenError):
        if "expired" in exc.message.lower():
            return TokenExpiredException(detail=exc.message)
        return InvalidTokenException(detail=exc.message)
    elif isinstance(exc, AuthorizationError):
        return InsufficientPermissionsException(detail=exc.message)
    else:
        return CredentialsException(detail=str(exc))