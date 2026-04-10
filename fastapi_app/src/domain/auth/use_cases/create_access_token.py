from datetime import timedelta
from src.resources.auth import create_access_token


class CreateAccessTokenUseCase:
    async def execute(
        self,
        login: str,
        user_id: int = None,
        is_superuser: bool = False,
        is_staff: bool = False,
        expires_delta: timedelta = None
    ) -> str:
        data = {
            "sub": str(user_id) if user_id else login,
            "username": login,
            "is_superuser": is_superuser,
            "is_staff": is_staff
        }
        
        token = create_access_token(data=data, expires_delta=expires_delta)
        return token