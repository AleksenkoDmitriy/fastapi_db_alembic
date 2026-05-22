from typing import Optional, List, Tuple
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from datetime import datetime
from sqlalchemy import func
from src.infrastructure.postgres.models.post import Post
from src.infrastructure.postgres.models.like import Like
from src.infrastructure.postgres.repositories.base import BaseRepository
from src.core.exceptions.infrastructure_exceptions import DatabaseError, IntegrityViolationError


class PostRepository(BaseRepository[Post]):
    def __init__(self):
        super().__init__(Post)
    
    def create(self, session: Session, **kwargs) -> Post:
        try:
            post = self.model(**kwargs)
            session.add(post)
            session.flush()
            return post
        except IntegrityError as e:
            raise IntegrityViolationError(
                f"Ошибка целостности при создании поста: {str(e)}",
                details={"kwargs": kwargs}
            )
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка БД при создании поста: {str(e)}", e)
    
    def update(self, session: Session, id: int, **kwargs) -> Optional[Post]:
        try:
            post = session.query(self.model).filter(self.model.id == id).first()
            if post:
                for key, value in kwargs.items():
                    setattr(post, key, value)
                session.flush()
            return post
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка БД при обновлении поста ID={id}: {str(e)}", e)
    
    def delete(self, session: Session, id: int) -> bool:
        try:
            post = session.query(self.model).filter(self.model.id == id).first()
            if post:
                session.delete(post)
                session.flush()
                return True
            return False
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка БД при удалении поста ID={id}: {str(e)}", e)
    
    def get_by_id(self, session: Session, id: int) -> Optional[Post]:
        try:
            return session.query(self.model).filter(self.model.id == id).first()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка БД при получении поста ID={id}: {str(e)}", e)
    
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
    
    def get_published_with_likes_count(
        self, 
        session: Session,
        skip: int = 0, 
        limit: int = 10,
        category_id: Optional[int] = None,
        location_id: Optional[int] = None
    ) -> List[Tuple[Post, int]]:
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
            ).group_by(Post.id)
            
            if category_id:
                query = query.filter(Post.category_id == category_id)
            
            if location_id:
                query = query.filter(Post.location_id == location_id)
            
            results = query.order_by(
                Post.pub_date.desc()
            ).offset(skip).limit(limit).all()
            
            return results
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка при получении постов с лайками: {str(e)}", e)
    
    def get_by_id_with_likes_count(self, session: Session, post_id: int) -> Optional[Tuple[Post, int]]:
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

    def get_by_category(self, session: Session, category_id: int) -> List[Post]:
        """Получить все посты категории"""
        try:
            return session.query(self.model).filter(
                self.model.category_id == category_id
            ).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка при получении постов категории ID={category_id}: {str(e)}", e)
    
    def get_posts_by_authors_with_likes_count(
        self, 
        session: Session, 
        author_ids: List[int], 
        skip: int = 0, 
        limit: int = 20
    ) -> List[Tuple[Post, int]]:
        """Получить посты авторов с количеством лайков"""
        try:
            query = session.query(
                Post,
                func.count(Like.id).label("likes_count")
            ).outerjoin(
                Like, Post.id == Like.post_id
            ).filter(
                Post.author_id.in_(author_ids),
                Post.is_published == True,
                Post.pub_date <= datetime.now()
            ).group_by(Post.id).order_by(
                Post.pub_date.desc()
            ).offset(skip).limit(limit)
            
            return query.all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка при получении постов авторов: {str(e)}", e)