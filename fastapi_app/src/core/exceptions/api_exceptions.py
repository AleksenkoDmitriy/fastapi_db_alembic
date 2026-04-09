from fastapi import Request, status
from fastapi.responses import JSONResponse
import logging

from src.core.exceptions.domain_exceptions import (
    DomainError, NotFoundError, DuplicateError, 
    ValidationError, BusinessRuleError
)
from src.core.exceptions.infrastructure_exceptions import DatabaseError, InfrastructureError

logger = logging.getLogger(__name__)


def register_exception_handlers(app):
    """Регистрация всех обработчиков исключений для FastAPI приложения"""
    
    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        logger.info(f"Not found: {exc.message}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": {
                    "code": 404, 
                    "message": exc.message, 
                    "details": exc.details,
                    "type": "not_found"
                }
            }
        )

    @app.exception_handler(DuplicateError)
    async def duplicate_handler(request: Request, exc: DuplicateError):
        logger.info(f"Duplicate: {exc.message}")
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "error": {
                    "code": 409, 
                    "message": exc.message, 
                    "details": exc.details,
                    "type": "duplicate"
                }
            }
        )

    @app.exception_handler(ValidationError)
    async def validation_error_handler(request: Request, exc: ValidationError):
        logger.info(f"Validation error: {exc.message}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "code": 422, 
                    "message": exc.message, 
                    "details": exc.details,
                    "type": "validation"
                }
            }
        )

    @app.exception_handler(BusinessRuleError)
    async def business_rule_handler(request: Request, exc: BusinessRuleError):
        logger.info(f"Business rule violation: {exc.message}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": {
                    "code": 400, 
                    "message": exc.message, 
                    "details": exc.details,
                    "type": "business_rule"
                }
            }
        )

    @app.exception_handler(DatabaseError)
    async def database_error_handler(request: Request, exc: DatabaseError):
        logger.error(f"Database error: {exc.message}", 
                    exc_info=exc.original_error if exc.original_error else True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": 500, 
                    "message": "Внутренняя ошибка сервера базы данных",
                    "type": "database"
                }
            }
        )

    @app.exception_handler(InfrastructureError)
    async def infrastructure_error_handler(request: Request, exc: InfrastructureError):
        logger.error(f"Infrastructure error: {exc.message}", 
                    exc_info=exc.original_error if exc.original_error else True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": 500, 
                    "message": "Внутренняя ошибка инфраструктуры",
                    "type": "infrastructure"
                }
            }
        )

    @app.exception_handler(DomainError)
    async def domain_error_handler(request: Request, exc: DomainError):
        logger.info(f"Domain error: {exc.message}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": {
                    "code": 400, 
                    "message": exc.message, 
                    "details": exc.details,
                    "type": "domain"
                }
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.exception(f"Unhandled exception: {type(exc).__name__}: {str(exc)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": 500, 
                    "message": "Внутренняя ошибка сервера",
                    "type": "internal"
                }
            }
        )