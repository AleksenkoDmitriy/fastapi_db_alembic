from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.core.user_logger import user_logger


class UserActionLoggingMiddleware(BaseHTTPMiddleware):
    EXCLUDED_PATHS = {"/", "/health", "/docs", "/openapi.json", "/redoc"}
    LOGGED_METHODS = {"POST", "PUT", "DELETE", "PATCH"}
    
    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.EXCLUDED_PATHS:
            return await call_next(request)
        
        response = await call_next(request)
        
        if request.method in self.LOGGED_METHODS:
            user_id = getattr(request.state, "user_id", None)
            username = getattr(request.state, "username", None)
            
            # Извлекаем тип ресурса (игнорируем api/v1)
            path_parts = [p for p in request.url.path.split("/") if p and p not in ["api", "v1"]]
            resource_type = path_parts[0] if path_parts else "unknown"
            resource_type = resource_type.rstrip('s')
            
            resource_id = None
            for part in path_parts:
                if part.isdigit():
                    resource_id = int(part)
                    break
            
            user_logger.log_action(
                user_id=user_id,
                username=username,
                action=request.method,
                resource_type=resource_type,
                resource_id=resource_id,
                ip_address=request.client.host if request.client else None,
                status="success" if 200 <= response.status_code < 300 else "error"
            )
        
        return response