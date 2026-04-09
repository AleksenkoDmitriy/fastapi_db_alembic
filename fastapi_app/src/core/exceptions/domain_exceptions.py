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