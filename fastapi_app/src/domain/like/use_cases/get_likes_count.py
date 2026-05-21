from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.like import LikeRepository

class GetLikesCountUseCase:
    def __init__(self):
        self.like_repo = LikeRepository()
    
    def execute(self, post_id: int) -> int:
        with database.session() as session:
            return self.like_repo.get_likes_count(session, post_id)