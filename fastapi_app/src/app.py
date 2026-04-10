import sys
from pathlib import Path
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

sys.path.append(str(Path(__file__).parent))

from src.api import categories, posts, comments, locations, users
from src.api import auth
from src.core.exceptions import register_exception_handlers


def create_app() -> FastAPI:
    app = FastAPI(root_path="/api/v1")

    register_exception_handlers(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
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

    return app