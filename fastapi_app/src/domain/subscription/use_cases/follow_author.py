from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.subscription import SubscriptionRepository
from src.infrastructure.postgres.repositories.users import UserRepository
from src.schemas.subscription import FollowResponse
from src.core.exceptions.domain_exceptions import NotFoundError, BusinessRuleError

class FollowAuthorUseCase:
    def __init__(self):
        self._database = database
        self._subscription_repo = SubscriptionRepository()
        self._user_repo = UserRepository()
    
    def execute(self, follower_id: int, following_id: int) -> FollowResponse:
        with self._database.session() as session:
            # Нельзя подписаться на себя
            if follower_id == following_id:
                raise BusinessRuleError(
                    "Нельзя подписаться на самого себя",
                    details={"user_id": follower_id}
                )
            
            # Проверяем, существует ли автор
            author = self._user_repo.get_by_id(session, following_id)
            if not author:
                raise NotFoundError(
                    entity_name="Пользователь",
                    field="id",
                    value=str(following_id)
                )
            
            # Проверяем, не подписан ли уже
            if self._subscription_repo.is_following(session, follower_id, following_id):
                raise BusinessRuleError(
                    f"Вы уже подписаны на пользователя {following_id}",
                    details={"follower_id": follower_id, "following_id": following_id}
                )
            
            # Подписываемся
            subscription = self._subscription_repo.follow(session, follower_id, following_id)
            session.commit()
            
            return FollowResponse(
                follower_id=subscription.follower_id,
                following_id=subscription.following_id,
                created_at=subscription.created_at
            )