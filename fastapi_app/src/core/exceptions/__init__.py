from src.core.exceptions.domain_exceptions import (
    DomainError,
    DuplicateError,
    NotFoundError,
    ValidationError,
    BusinessRuleError,
    AuthenticationError,
    AuthorizationError,
    TokenError,
    UserNotFoundByLoginException,
    WrongPasswordException,
)

from src.core.exceptions.infrastructure_exceptions import (
    InfrastructureError,
    DatabaseError,
    RepositoryError,
)

from src.core.exceptions.auth_exceptions import (
    CredentialsException,
    TokenExpiredException,
    InvalidTokenException,
    InsufficientPermissionsException,
    UserNotFoundException,
    UserInactiveException,
    InvalidPasswordException,
    handle_domain_auth_error,
)

from src.core.exceptions.api_exceptions import register_exception_handlers

__all__ = [
    # Domain exceptions
    "DomainError",
    "DuplicateError",
    "NotFoundError",
    "ValidationError",
    "BusinessRuleError",
    "AuthenticationError",
    "AuthorizationError",
    "TokenError",
    "UserNotFoundByLoginException",
    "WrongPasswordException",
    # Infrastructure exceptions
    "InfrastructureError",
    "DatabaseError",
    "RepositoryError",
    # API auth exceptions
    "CredentialsException",
    "TokenExpiredException",
    "InvalidTokenException",
    "InsufficientPermissionsException",
    "UserNotFoundException",
    "UserInactiveException",
    "InvalidPasswordException",
    "handle_domain_auth_error",
    # Handlers
    "register_exception_handlers",
]