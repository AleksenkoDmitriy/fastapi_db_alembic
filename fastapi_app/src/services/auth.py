import os
from pydantic import SecretStr
from datetime import timedelta

class Settings:
    SECRET_KEY: SecretStr = SecretStr(os.getenv("SECRET_KEY", "your-secret-key-change-in-production-min-32-chars"))
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 1

settings = Settings()

SECRET_AUTH_KEY = settings.SECRET_KEY
AUTH_ALGORITHM = settings.ALGORITHM