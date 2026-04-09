from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from datetime import datetime
from src.infrastructure.sqlite.models.users import User
from src.infrastructure.sqlite.repositories.base import BaseRepository
from src.core.exceptions.infrastructure_exceptions import DatabaseError


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)
    
    def create(self, session: Session, **kwargs) -> User:
        try:
            if 'is_superuser' not in kwargs:
                kwargs['is_superuser'] = False
            if 'is_staff' not in kwargs:
                kwargs['is_staff'] = False
            if 'is_active' not in kwargs:
                kwargs['is_active'] = True
            if 'date_joined' not in kwargs:
                kwargs['date_joined'] = datetime.now()
                
            return super().create(session, **kwargs)
        except DatabaseError as e:
            raise
        except IntegrityError as e:
            session.rollback()
            if "UNIQUE constraint failed" in str(e):
                if "username" in str(e):
                    raise DatabaseError("Пользователь с таким именем уже существует", e)
                elif "email" in str(e):
                    raise DatabaseError("Пользователь с таким email уже существует", e)
            raise DatabaseError(f"Ошибка при создании пользователя: {str(e)}", e)
    
    def get_by_username(self, session: Session, username: str) -> Optional[User]:
        try:
            return session.query(self.model).filter(
                self.model.username == username
            ).first()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка при поиске пользователя по имени '{username}': {str(e)}", e)
    
    def get_by_email(self, session: Session, email: str) -> Optional[User]:
        try:
            return session.query(self.model).filter(
                self.model.email == email
            ).first()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Ошибка при поиске пользователя по email '{email}': {str(e)}", e)
    
    def get_by_login(self, session: Session, login: str) -> Optional[User]:
        """Получение пользователя по логину (username)"""
        return self.get_by_username(session, login)