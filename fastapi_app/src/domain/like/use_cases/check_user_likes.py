from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.like import LikeRepository

class CheckUserLikeUseCase:
    def __init__(self):
        self.like_repo = LikeRepository()
    
    def execute(self, user_id: int, post_id: int) -> bool:
        with database.session() as session:
            like = self.like_repo.get_like(session, user_id, post_id)
            return like is not None