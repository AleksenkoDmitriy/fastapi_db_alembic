from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.like import LikeRepository
from src.infrastructure.postgres.repositories.posts import PostRepository
from src.core.exceptions.domain_exceptions import NotFoundError, BusinessRuleError

class AddLikeUseCase:
    def __init__(self):
        self.like_repo = LikeRepository()
        self.post_repo = PostRepository()
    
    def execute(self, user_id: int, post_id: int):
        with database.session() as session:
            post = self.post_repo.get_by_id(session, post_id)
            if not post:
                raise NotFoundError("Post", "id", str(post_id))
            
            existing_like = self.like_repo.get_like(session, user_id, post_id)
            if existing_like:
                raise BusinessRuleError(
                    "Вы уже лайкнули этот пост",
                    details={"user_id": user_id, "post_id": post_id}
                )
            
            like = self.like_repo.add_like(session, user_id, post_id)
            session.commit()
            session.refresh(like)
            return like