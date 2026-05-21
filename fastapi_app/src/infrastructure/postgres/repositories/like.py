from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from src.infrastructure.postgres.models import Like
from src.infrastructure.postgres.repositories.base import BaseRepository
from src.core.exceptions.infrastructure_exceptions import DatabaseError, IntegrityViolationError

class LikeRepository(BaseRepository[Like]):
    def __init__(self):
        super().__init__(Like)
    
    def add_like(self, session: Session, user_id: int, post_id: int) -> Like:
        try:
            like = Like(user_id=user_id, post_id=post_id)
            session.add(like)
            session.flush()
            return like
        except IntegrityError as e:
            if "unique_post_user_like" in str(e) or "duplicate" in str(e).lower():
                raise IntegrityViolationError(
                    f"Пользователь {user_id} уже лайкнул пост {post_id}",
                    details={"user_id": user_id, "post_id": post_id}
                )
            raise DatabaseError(f"Ошибка целостности БД при добавлении лайка: {str(e)}")
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка БД при добавлении лайка: {str(e)}")
    
    def remove_like(self, session: Session, user_id: int, post_id: int) -> bool:
        try:
            like = session.query(self.model).filter(
                self.model.user_id == user_id,
                self.model.post_id == post_id
            ).first()
            
            if like:
                session.delete(like)
                session.flush()
                return True
            return False
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка БД при удалении лайка: {str(e)}")
    
    def get_like(self, session: Session, user_id: int, post_id: int) -> Optional[Like]:
        try:
            return session.query(self.model).filter(
                self.model.user_id == user_id,
                self.model.post_id == post_id
            ).first()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка БД при получении лайка: {str(e)}")
    
    def get_likes_count(self, session: Session, post_id: int) -> int:
        try:
            from sqlalchemy import func
            return session.query(func.count(self.model.id)).filter(
                self.model.post_id == post_id
            ).scalar() or 0
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка БД при подсчете лайков поста {post_id}: {str(e)}")
    
    def get_user_liked_posts(self, session: Session, user_id: int) -> List[int]:
        try:
            likes = session.query(self.model).filter(
                self.model.user_id == user_id
            ).all()
            return [like.post_id for like in likes]
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка БД при получении лайков пользователя {user_id}: {str(e)}")