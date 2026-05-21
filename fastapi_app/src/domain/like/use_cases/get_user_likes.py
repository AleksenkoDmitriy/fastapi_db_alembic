from typing import List
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.like import LikeRepository

class GetUserLikesUseCase:
    def __init__(self):
        self.like_repo = LikeRepository()
    
    def execute(self, user_id: int) -> List[int]:
        with database.session() as session:
            return self.like_repo.get_user_liked_posts(session, user_id)