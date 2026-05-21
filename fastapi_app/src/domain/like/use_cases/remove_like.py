from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.like import LikeRepository
from src.core.exceptions.domain_exceptions import NotFoundError, AuthorizationError

class RemoveLikeUseCase:
    def __init__(self):
        self.like_repo = LikeRepository()
    
    def execute(self, user_id: int, post_id: int):
        with database.session() as session:
            like = self.like_repo.get_like(session, user_id, post_id)
            if not like:
                raise NotFoundError("Like", "user_id and post_id", f"{user_id}, {post_id}")
            
            if like.user_id != user_id:
                raise AuthorizationError("Вы можете удалить только свой лайк")
            
            self.like_repo.remove_like(session, user_id, post_id)
            session.commit()
            return True