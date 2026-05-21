from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from src.infrastructure.postgres.models.post import Post
from src.infrastructure.postgres.repositories.base import BaseRepository
from src.core.exceptions.infrastructure_exceptions import DatabaseError
from src.infrastructure.postgres.models.like import Like
from sqlalchemy import func

class PostRepository(BaseRepository[Post]):
    def __init__(self):
        super().__init__(Post)
    
    def get_by_id_with_relations(self, session: Session, id: int) -> Optional[Post]:
        try:
            return session.query(self.model).options(
                joinedload(self.model.author),
                joinedload(self.model.category),
                joinedload(self.model.location)
            ).filter(self.model.id == id).first()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка при получении поста ID={id} со связями: {str(e)}", e)
    
    def get_published(
        self, 
        session: Session,
        skip: int = 0, 
        limit: int = 10,
        category_id: Optional[int] = None,
        location_id: Optional[int] = None
    ) -> List[Post]:
        try:
            query = session.query(self.model).filter(
                self.model.is_published == True,
                self.model.pub_date <= datetime.now()
            )
            
            if category_id:
                query = query.filter(self.model.category_id == category_id)
            
            if location_id:
                query = query.filter(self.model.location_id == location_id)
            
            return query.order_by(
                self.model.pub_date.desc()
            ).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка при получении опубликованных постов: {str(e)}", e)
    
    def get_by_author(self, session: Session, author_id: int) -> List[Post]:
        try:
            return session.query(self.model).filter(
                self.model.author_id == author_id
            ).options(
                joinedload(self.model.category),
                joinedload(self.model.location)
            ).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка при получении постов автора ID={author_id}: {str(e)}", e)
    
    def get_by_category(self, session: Session, category_id: int) -> List[Post]:
        try:
            return session.query(self.model).filter(
                self.model.category_id == category_id,
                self.model.is_published == True,
                self.model.pub_date <= datetime.now()
            ).options(
                joinedload(self.model.author)
            ).order_by(self.model.pub_date.desc()).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка при получении постов категории ID={category_id}: {str(e)}", e)
    
    def search(self, session: Session, search_term: str) -> List[Post]:
        try:
            return session.query(self.model).filter(
                self.model.is_published == True,
                self.model.pub_date <= datetime.now()
            ).filter(
                (self.model.title.contains(search_term)) |
                (self.model.text.contains(search_term))
            ).options(
                joinedload(self.model.author),
                joinedload(self.model.category)
            ).order_by(self.model.pub_date.desc()).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка при поиске постов по запросу '{search_term}': {str(e)}", e)
        
    def get_published_with_likes_count(
        self, 
        session: Session,
        skip: int = 0, 
        limit: int = 10,
        category_id: Optional[int] = None,
        location_id: Optional[int] = None
    ) -> List[tuple]:
        """Получить опубликованные посты с количеством лайков"""
        try:
            query = session.query(
                Post,
                func.count(Like.id).label("likes_count")
            ).outerjoin(
                Like, Post.id == Like.post_id
            ).filter(
                Post.is_published == True,
                Post.pub_date <= datetime.now()
            )
            
            if category_id:
                query = query.filter(Post.category_id == category_id)
            
            if location_id:
                query = query.filter(Post.location_id == location_id)
            
            results = query.group_by(Post.id).order_by(
                Post.pub_date.desc()
            ).offset(skip).limit(limit).all()
            
            return results
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка при получении постов с лайками: {str(e)}", e)
    
    def get_by_id_with_likes_count(self, session: Session, post_id: int) -> Optional[tuple]:
        """Получить пост по ID с количеством лайков"""
        try:
            result = session.query(
                Post,
                func.count(Like.id).label("likes_count")
            ).outerjoin(
                Like, Post.id == Like.post_id
            ).filter(
                Post.id == post_id
            ).group_by(Post.id).first()
            
            return result
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка при получении поста ID={post_id} с лайками: {str(e)}", e)