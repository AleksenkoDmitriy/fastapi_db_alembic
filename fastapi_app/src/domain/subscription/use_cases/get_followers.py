from typing import List
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.subscription import SubscriptionRepository
from src.infrastructure.postgres.repositories.users import UserRepository
from src.schemas.subscription import FollowersResponse
from src.core.exceptions.domain_exceptions import DomainError
from src.core.exceptions.infrastructure_exceptions import DatabaseError


class GetFollowersUseCase:
    def __init__(self):
        self._database = database
        self._subscription_repo = SubscriptionRepository()
        self._user_repo = UserRepository()
    
    def execute(self, user_id: int, skip: int = 0, limit: int = 50) -> List[FollowersResponse]:
        try:
            with self._database.session() as session:
                # Получаем ID подписчиков
                follower_ids = self._subscription_repo.get_followers(session, user_id, skip, limit)
                
                result = []
                for follower_id in follower_ids:
                    user = self._user_repo.get_by_id(session, follower_id)
                    if user:
                        # Получаем время подписки
                        subscription = session.query(self._subscription_repo.model).filter(
                            self._subscription_repo.model.follower_id == follower_id,
                            self._subscription_repo.model.following_id == user_id
                        ).first()
                        
                        result.append(FollowersResponse(
                            user_id=user.id,
                            username=user.username,
                            email=user.email,
                            followed_at=subscription.created_at if subscription else None
                        ))
                
                return result
        
        except DatabaseError as e:
            raise DomainError(
                "Ошибка базы данных при получении подписчиков",
                details={"user_id": user_id, "error": str(e)}
            )