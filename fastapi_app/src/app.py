import sys
from pathlib import Path
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

sys.path.append(str(Path(__file__).parent))

from src.api import categories, posts, comments, locations, users
from src.api import auth
from src.core.exceptions import register_exception_handlers
from src.core.config import settings

def create_app() -> FastAPI:
    app = FastAPI(
        root_path=settings.ROOT_PATH,
        title=settings.APP_NAME,
        description="API для блога с JWT авторизацией",
        version=settings.APP_VERSION,
        debug=settings.DEBUG
    )
    
    register_exception_handlers(app)

    origins = settings.ORIGINS.split(",") if "," in settings.ORIGINS else [settings.ORIGINS]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(categories.router)
    app.include_router(posts.router) 
    app.include_router(comments.router)
    app.include_router(locations.router)
    app.include_router(users.router)
    app.include_router(auth.router)
    
    @app.get("/")
    async def root():
        return {
            "message": f"Welcome to {settings.APP_NAME}",
            "version": settings.APP_VERSION,
            "docs": f"{settings.ROOT_PATH}/docs"
        }
    
    @app.get("/health")
    async def health_check():
        return {"status": "ok", "version": settings.APP_VERSION}

    return app