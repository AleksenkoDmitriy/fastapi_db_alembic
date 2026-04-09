from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.infrastructure.sqlite.models.category import Category
from src.infrastructure.sqlite.repositories.base import BaseRepository
from src.core.exceptions.infrastructure_exceptions import DatabaseError


class CategoryRepository(BaseRepository[Category]):
    def __init__(self):
        super().__init__(Category)
    
    def get_by_slug(self, session: Session, slug: str) -> Optional[Category]:
        try:
            return session.query(self.model).filter(self.model.slug == slug).first()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка при поиске по slug '{slug}': {str(e)}", e)
    
    def get_published(self, session: Session, skip: int = 0, limit: int = 100) -> List[Category]:
        try:
            return session.query(self.model).filter(
                self.model.is_published == True
            ).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка при получении опубликованных категорий: {str(e)}", e)
    
    def search_by_title(self, session: Session, title: str) -> List[Category]:
        try:
            return session.query(self.model).filter(self.model.title.contains(title)).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка при поиске по названию '{title}': {str(e)}", e)