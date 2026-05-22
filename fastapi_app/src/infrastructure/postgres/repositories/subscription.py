from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import func
from src.infrastructure.postgres.models.subscription import Subscription
from src.infrastructure.postgres.repositories.base import BaseRepository
from src.core.exceptions.infrastructure_exceptions import DatabaseError, IntegrityViolationError


class SubscriptionRepository(BaseRepository[Subscription]):
    def __init__(self):
        super().__init__(Subscription)
    
    def follow(self, session: Session, follower_id: int, following_id: int) -> Subscription:
        """Подписаться на автора"""
        try:
            subscription = Subscription(
                follower_id=follower_id,
                following_id=following_id
            )
            session.add(subscription)
            session.flush()
            return subscription
        except IntegrityError as e:
            raise IntegrityViolationError(
                f"Пользователь {follower_id} уже подписан на автора {following_id}",
                details={"follower_id": follower_id, "following_id": following_id}
            )
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка БД при создании подписки: {str(e)}", e)
    
    def unfollow(self, session: Session, follower_id: int, following_id: int) -> bool:
        """Отписаться от автора"""
        try:
            subscription = session.query(self.model).filter(
                self.model.follower_id == follower_id,
                self.model.following_id == following_id
            ).first()
            
            if subscription:
                session.delete(subscription)
                session.flush()
                return True
            return False
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка БД при удалении подписки: {str(e)}", e)
    
    def is_following(self, session: Session, follower_id: int, following_id: int) -> bool:
        """Проверить, подписан ли пользователь на автора"""
        try:
            subscription = session.query(self.model).filter(
                self.model.follower_id == follower_id,
                self.model.following_id == following_id
            ).first()
            return subscription is not None
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка БД при проверке подписки: {str(e)}", e)
    
    def get_following(self, session: Session, follower_id: int, skip: int = 0, limit: int = 50) -> List[int]:
        """Получить ID авторов, на которых подписан пользователь"""
        try:
            subscriptions = session.query(self.model).filter(
                self.model.follower_id == follower_id
            ).offset(skip).limit(limit).all()
            return [s.following_id for s in subscriptions]
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка БД при получении подписок пользователя: {str(e)}", e)
    
    def get_followers(self, session: Session, following_id: int, skip: int = 0, limit: int = 50) -> List[int]:
        """Получить ID подписчиков автора"""
        try:
            subscriptions = session.query(self.model).filter(
                self.model.following_id == following_id
            ).offset(skip).limit(limit).all()
            return [s.follower_id for s in subscriptions]
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка БД при получении подписчиков автора: {str(e)}", e)
    
    def get_following_count(self, session: Session, follower_id: int) -> int:
        """Получить количество подписок пользователя"""
        try:
            return session.query(func.count(self.model.id)).filter(
                self.model.follower_id == follower_id
            ).scalar() or 0
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка БД при подсчёте подписок: {str(e)}", e)
    
    def get_followers_count(self, session: Session, following_id: int) -> int:
        """Получить количество подписчиков автора"""
        try:
            return session.query(func.count(self.model.id)).filter(
                self.model.following_id == following_id
            ).scalar() or 0
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка БД при подсчёте подписчиков: {str(e)}", e)