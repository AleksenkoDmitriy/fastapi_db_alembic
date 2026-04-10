class DomainError(Exception):
    """Базовое исключение для доменного слоя"""
    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(message)


class DuplicateError(DomainError):
    """Ошибка дублирования данных"""
    def __init__(self, entity_name: str, field: str, value: str):
        message = f"{entity_name} с {field} '{value}' уже существует"
        details = {"entity": entity_name, "field": field, "value": value}
        super().__init__(message, details)


class NotFoundError(DomainError):
    """Объект не найден"""
    def __init__(self, entity_name: str, field: str, value: str):
        message = f"{entity_name} с {field} '{value}' не найдена"
        details = {"entity": entity_name, "field": field, "value": value}
        super().__init__(message, details)


class ValidationError(DomainError):
    """Ошибка валидации бизнес-правил"""
    pass


class BusinessRuleError(DomainError):
    """Нарушение бизнес-правил"""
    pass


class AuthenticationError(DomainError):
    """Ошибка аутентификации"""
    def __init__(self, message: str = "Неверное имя пользователя или пароль"):
        super().__init__(message, {"reason": "invalid_credentials"})


class AuthorizationError(DomainError):
    """Ошибка авторизации"""
    def __init__(self, message: str = "Недостаточно прав для выполнения операции"):
        super().__init__(message, {"reason": "insufficient_permissions"})


class TokenError(DomainError):
    """Ошибка работы с токеном"""
    def __init__(self, message: str = "Недействительный токен"):
        super().__init__(message, {"reason": "invalid_token"})


class UserNotFoundByLoginException(AuthenticationError):
    """Пользователь не найден по логину"""
    def __init__(self, login: str):
        super().__init__(f"Пользователь с логином '{login}' не найден")
        self.login = login
    
    def get_detail(self):
        return {"message": self.message, "type": "user_not_found", "login": self.login}


class WrongPasswordException(AuthenticationError):
    """Неверный пароль"""
    def __init__(self):
        super().__init__("Неверный пароль")
    
    def get_detail(self):
        return {"message": self.message, "type": "wrong_password"}