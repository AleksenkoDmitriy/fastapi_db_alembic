from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from src.infrastructure.postgres.models.category import Category
from src.infrastructure.postgres.repositories.base import BaseRepository
from src.core.exceptions.infrastructure_exceptions import DatabaseError, ForeignKeyViolationError


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
        
    def delete(self, session: Session, id: int) -> bool:
        try:
            category = session.query(self.model).filter(self.model.id == id).first()
            if category:
                session.delete(category)
                session.flush()
                return True
            return False
        except IntegrityError as e:
            if "foreign key" in str(e).lower() or "not null" in str(e).lower():
                raise ForeignKeyViolationError(
                    f"Невозможно удалить категорию ID={id}, так как она используется",
                    details={"category_id": id, "original_error": str(e)}
                )
            raise DatabaseError(f"Ошибка целостности при удалении категории ID={id}: {str(e)}", e)
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка БД при удалении категории ID={id}: {str(e)}", e)