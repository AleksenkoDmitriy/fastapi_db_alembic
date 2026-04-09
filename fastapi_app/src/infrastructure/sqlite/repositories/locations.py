from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.infrastructure.sqlite.models.location import Location
from src.infrastructure.sqlite.repositories.base import BaseRepository
from src.core.exceptions.infrastructure_exceptions import DatabaseError


class LocationRepository(BaseRepository[Location]):
    def __init__(self):
        super().__init__(Location)
    
    def get_published(self, session: Session, skip: int = 0, limit: int = 100) -> List[Location]:
        try:
            return session.query(self.model).filter(
                self.model.is_published == True
            ).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка при получении опубликованных локаций: {str(e)}", e)
    
    def get_by_name(self, session: Session, name: str) -> Optional[Location]:
        try:
            return session.query(self.model).filter(self.model.name == name).first()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка при поиске локации по имени '{name}': {str(e)}", e)