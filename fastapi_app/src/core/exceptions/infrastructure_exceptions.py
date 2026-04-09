class InfrastructureError(Exception):
    """Базовое исключение для инфраструктурного слоя"""
    def __init__(self, message: str, original_error: Exception = None):
        self.message = message
        self.original_error = original_error
        super().__init__(message)


class DatabaseError(InfrastructureError):
    """Ошибка базы данных"""
    pass


class RepositoryError(InfrastructureError):
    """Ошибка репозитория"""
    pass