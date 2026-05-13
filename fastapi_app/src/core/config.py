import logging
import os
import sys

from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Blog API"
    APP_VERSION: str = "1.0.0"

    DEBUG: bool = True

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    ROOT_PATH: str = "/api/v1"
    ORIGINS: str = "*"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    AUTH_ALGORITHM: str = "HS256"
    SECRET_AUTH_KEY: str

    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "blog"
    POSTGRES_USER: str = "blog"
    POSTGRES_PASSWORD: str = "blogpass"

    POSTGRES_RECONNECT_INTERVAL_SEC: int = 1

    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: Optional[str] = None
    
    @property
    def database_url(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = "/fastapi_app/.env"
        extra = "ignore"

settings = Settings()


def setup_logging() -> None:
    handlers = [logging.StreamHandler(sys.stdout)]

    if settings.LOG_FILE:
        os.makedirs(
            os.path.dirname(settings.LOG_FILE),
            exist_ok=True
        )

        handlers.append(
            logging.FileHandler(settings.LOG_FILE)
        )

    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format=settings.LOG_FORMAT,
        handlers=handlers,
    )

    logging.getLogger("uvicorn.access").setLevel(
        logging.WARNING
    )

    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.WARNING
    )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)