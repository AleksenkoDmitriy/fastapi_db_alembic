from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.subscription import SubscriptionRepository
from src.core.exceptions.domain_exceptions import NotFoundError


class UnfollowAuthorUseCase:
    def __init__(self):
        self._database = database
        self._subscription_repo = SubscriptionRepository()
    
    def execute(self, follower_id: int, following_id: int) -> bool:
        with self._database.session() as session:
            # Проверяем, подписан ли
            if not self._subscription_repo.is_following(session, follower_id, following_id):
                raise NotFoundError(
                    entity_name="Подписка",
                    field="following_id",
                    value=str(following_id)
                )
            
            # Отписываемся
            result = self._subscription_repo.unfollow(session, follower_id, following_id)
            session.commit()
            return result