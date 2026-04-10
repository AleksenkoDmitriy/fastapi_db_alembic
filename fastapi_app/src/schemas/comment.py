from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from .users import User


class Comment(BaseModel):
    id: Optional[int] = None
    post_id: int
    author: User
    text: str
    created_at: datetime = Field(default_factory=datetime.now)
    
    @field_validator('text')
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Текст комментария не может быть пустым')
        if len(v.strip()) < 2:
            raise ValueError('Текст комментария должен содержать минимум 2 символа')
        if len(v.strip()) > 1000:
            raise ValueError('Текст комментария не может превышать 1000 символов')
        return v.strip()
    
    class Config:
        from_attributes = True


class CommentCreate(BaseModel):
    post_id: int
    text: str
    
    @field_validator('post_id')
    @classmethod
    def validate_post_id(cls, v: int) -> int:
        if v <= 0:
            raise ValueError('ID поста должен быть положительным числом')
        return v
    
    @field_validator('text')
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Текст комментария не может быть пустым')
        if len(v.strip()) < 2:
            raise ValueError('Текст комментария должен содержать минимум 2 символа')
        if len(v.strip()) > 1000:
            raise ValueError('Текст комментария не может превышать 1000 символов')
        return v.strip()


class CommentUpdate(BaseModel):
    text: Optional[str] = None
    
    @field_validator('text')
    @classmethod
    def validate_text(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.strip():
                raise ValueError('Текст комментария не может быть пустым')
            if len(v.strip()) < 2:
                raise ValueError('Текст комментария должен содержать минимум 2 символа')
            if len(v.strip()) > 1000:
                raise ValueError('Текст комментария не может превышать 1000 символов')
            return v.strip()
        return v