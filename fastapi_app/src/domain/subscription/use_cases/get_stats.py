from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.subscription import SubscriptionRepository
from src.infrastructure.postgres.repositories.users import UserRepository
from src.schemas.subscription import SubscriptionStats
from src.core.exceptions.domain_exceptions import NotFoundError, DomainError
from src.core.exceptions.infrastructure_exceptions import DatabaseError


class GetSubscriptionStatsUseCase:
    def __init__(self):
        self._database = database
        self._subscription_repo = SubscriptionRepository()
        self._user_repo = UserRepository()
    
    def execute(self, user_id: int, current_user_id: int = None) -> SubscriptionStats:
        try:
            with self._database.session() as session:
                # Проверяем, существует ли пользователь
                user = self._user_repo.get_by_id(session, user_id)
                if not user:
                    raise NotFoundError(
                        entity_name="Пользователь",
                        field="id",
                        value=str(user_id)
                    )
                
                # Получаем статистику
                followers_count = self._subscription_repo.get_followers_count(session, user_id)
                following_count = self._subscription_repo.get_following_count(session, user_id)
                
                # Проверяем, подписан ли текущий пользователь на этого автора
                is_following = False
                if current_user_id:
                    is_following = self._subscription_repo.is_following(
                        session, current_user_id, user_id
                    )
                
                return SubscriptionStats(
                    followers_count=followers_count,
                    following_count=following_count,
                    is_following=is_following
                )
        
        except NotFoundError:
            raise
        except DatabaseError as e:
            raise DomainError(
                "Ошибка базы данных при получении статистики подписок",
                details={"user_id": user_id, "error": str(e)}
            )