from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from src.infrastructure.postgres.models.post_like import PostLike
from src.infrastructure.postgres.repositories.base import BaseRepository
from src.core.exceptions.infrastructure_exceptions import DatabaseError, IntegrityViolationError


class LikeRepository(BaseRepository[PostLike]):
    def __init__(self):
        super().__init__(PostLike)

    def add_like(self, session: Session, user_id: int, post_id: int) -> PostLike:
        try:
            like = self.create(session, user_id=user_id, post_id=post_id)
            return like
        except IntegrityError as e:
            raise IntegrityViolationError(
                f"Пользователь {user_id} уже лайкнул пост {post_id}",
                details={"user_id": user_id, "post_id": post_id}
            )
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка при добавлении лайка: {str(e)}")

    def remove_like(self, session: Session, user_id: int, post_id: int) -> bool:
        try:
            like = session.query(self.model).filter(
                self.model.user_id == user_id,
                self.model.post_id == post_id
            ).first()
            if like:
                session.delete(like)
                return True
            return False
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка при удалении лайка: {str(e)}")

    def get_like(self, session: Session, user_id: int, post_id: int) -> Optional[PostLike]:
        try:
            return session.query(self.model).filter(
                self.model.user_id == user_id,
                self.model.post_id == post_id
            ).first()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка при получении лайка: {str(e)}")

    def get_likes_count(self, session: Session, post_id: int) -> int:
        try:
            return session.query(self.model).filter(
                self.model.post_id == post_id
            ).count()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка при подсчёте лайков поста {post_id}: {str(e)}")

    def get_user_liked_posts(self, session: Session, user_id: int) -> List[int]:
        try:
            likes = session.query(self.model).filter(
                self.model.user_id == user_id
            ).all()
            return [like.post_id for like in likes]
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка при получении лайков пользователя {user_id}: {str(e)}")