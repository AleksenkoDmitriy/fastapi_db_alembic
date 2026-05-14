import logging
import os
import sys
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv('/fastapi_db/.env')

class Settings(BaseSettings):
    APP_NAME: str = os.getenv('APP_NAME', 'FastAPI Blog API')
    APP_VERSION: str = os.getenv('APP_VERSION', '1.0.0')
    DEBUG: bool = os.getenv('DEBUG', 'True').lower() == 'true'
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', '8000'))
    ROOT_PATH: str = os.getenv('ROOT_PATH', '/api/v1')
    ORIGINS: str = os.getenv('ORIGINS', '*')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))
    AUTH_ALGORITHM: str = os.getenv('AUTH_ALGORITHM', 'HS256')
    SECRET_AUTH_KEY: str = os.getenv('SECRET_AUTH_KEY', '')
    POSTGRES_HOST: str = os.getenv('POSTGRES_HOST', 'db')
    POSTGRES_PORT: int = int(os.getenv('POSTGRES_PORT', '5432'))
    POSTGRES_DB: str = os.getenv('POSTGRES_DB', 'blog')
    POSTGRES_USER: str = os.getenv('POSTGRES_USER', 'blog')
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD', 'blogpass')
    POSTGRES_RECONNECT_INTERVAL_SEC: int = int(os.getenv('POSTGRES_RECONNECT_INTERVAL_SEC', '1'))
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT: str = os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    LOG_FILE: Optional[str] = os.getenv('LOG_FILE')
    USER_ACTION_LOG_FILE: Optional[str] = os.getenv('USER_ACTION_LOG_FILE', '/fastapi_app/logs/user_actions.log')

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    UPLOAD_DIR: str = "/fastapi_app/uploads"
    
    class Config:
        extra = "ignore"


settings = Settings()


def setup_logging() -> None:
    handlers = [logging.StreamHandler(sys.stdout)]

    if settings.LOG_FILE:
        os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)
        handlers.append(logging.FileHandler(settings.LOG_FILE))

    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format=settings.LOG_FORMAT,
        handlers=handlers,
    )

    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)