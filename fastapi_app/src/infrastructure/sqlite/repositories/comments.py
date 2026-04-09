from typing import List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from src.infrastructure.sqlite.models.comment import Comment
from src.infrastructure.sqlite.repositories.base import BaseRepository
from src.core.exceptions.infrastructure_exceptions import DatabaseError


class CommentRepository(BaseRepository[Comment]):
    def __init__(self):
        super().__init__(Comment)
    
    def get_by_post(self, session: Session, post_id: int) -> List[Comment]:
        try:
            return session.query(self.model).filter(
                self.model.post_id == post_id
            ).options(
                joinedload(self.model.author)
            ).order_by(self.model.created_at.desc()).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка при получении комментариев поста ID={post_id}: {str(e)}", e)
    
    def get_by_author(self, session: Session, author_id: int) -> List[Comment]:
        try:
            return session.query(self.model).filter(
                self.model.author_id == author_id
            ).options(
                joinedload(self.model.post)
            ).order_by(self.model.created_at.desc()).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка при получении комментариев автора ID={author_id}: {str(e)}", e)
    
    def get_recent(self, session: Session, limit: int = 10) -> List[Comment]:
        try:
            return session.query(self.model).options(
                joinedload(self.model.author),
                joinedload(self.model.post)
            ).order_by(self.model.created_at.desc()).limit(limit).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка при получении последних комментариев: {str(e)}", e)