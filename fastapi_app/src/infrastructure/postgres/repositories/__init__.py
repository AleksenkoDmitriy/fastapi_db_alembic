from src.infrastructure.postgres.repositories.users import UserRepository
from src.infrastructure.postgres.repositories.categories import CategoryRepository
from src.infrastructure.postgres.repositories.locations import LocationRepository
from src.infrastructure.postgres.repositories.posts import PostRepository
from src.infrastructure.postgres.repositories.comments import CommentRepository

__all__ = [
    "UserRepository",
    "CategoryRepository",
    "LocationRepository",
    "PostRepository",
    "CommentRepository"
]