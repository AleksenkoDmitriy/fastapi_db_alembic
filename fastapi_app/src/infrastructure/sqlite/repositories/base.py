from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError as SQLAlchemyIntegrityError
from sqlalchemy.exc import SQLAlchemyError
from src.core.exceptions.infrastructure_exceptions import DatabaseError

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def get_by_id(self, session: Session, id: int) -> Optional[ModelType]:
        try:
            return session.query(self.model).filter(self.model.id == id).first()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка при получении записи ID={id}: {str(e)}", e)
    
    def get_all(self, session: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        try:
            return session.query(self.model).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка при получении списка: {str(e)}", e)
    
    def create(self, session: Session, **kwargs) -> ModelType:
        try:
            obj = self.model(**kwargs)
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj
        except SQLAlchemyIntegrityError as e:
            session.rollback()
            if "UNIQUE constraint failed" in str(e):
                raise DatabaseError("Запись с такими данными уже существует", e)
            raise DatabaseError(f"Ошибка целостности данных: {str(e)}", e)
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseError(f"Ошибка при создании записи: {str(e)}", e)
    
    def update(self, session: Session, id: int, **kwargs) -> Optional[ModelType]:
        try:
            obj = self.get_by_id(session, id)
            if obj:
                for key, value in kwargs.items():
                    if hasattr(obj, key) and value is not None:
                        setattr(obj, key, value)
                session.commit()
                session.refresh(obj)
            return obj
        except SQLAlchemyIntegrityError as e:
            session.rollback()
            if "UNIQUE constraint failed" in str(e):
                raise DatabaseError("Запись с такими данными уже существует", e)
            raise DatabaseError(f"Ошибка целостности данных: {str(e)}", e)
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseError(f"Ошибка при обновлении записи ID={id}: {str(e)}", e)
    
    def delete(self, session: Session, id: int) -> bool:
        try:
            obj = self.get_by_id(session, id)
            if obj:
                session.delete(obj)
                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseError(f"Ошибка при удалении записи ID={id}: {str(e)}", e)
    
    def count(self, session: Session) -> int:
        try:
            return session.query(func.count(self.model.id)).scalar()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка при подсчёте записей: {str(e)}", e)