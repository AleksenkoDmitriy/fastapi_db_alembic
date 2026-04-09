from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
import re


class BaseModelSchema(BaseModel):
    is_published: bool = Field(
        True, 
        description="Опубликовано. Снимите галочку, чтобы скрыть публикацию."
    )
    created_at: datetime = Field(default_factory=datetime.now)


class Category(BaseModelSchema):
    id: Optional[int] = None
    title: str = Field(max_length=256)
    description: str
    slug: str = Field(
        pattern=r'^[a-zA-Z0-9_-]+$',
        description="Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание."
    )
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Валидация названия категории"""
        if not v or not v.strip():
            raise ValueError('Название категории не может быть пустым')
        if len(v.strip()) < 3:
            raise ValueError('Название категории должно содержать минимум 3 символа')
        return v.strip()
    
    @field_validator('slug')
    @classmethod
    def validate_slug(cls, v: str) -> str:
        """Валидация slug"""
        if not v or not v.strip():
            raise ValueError('Slug не может быть пустым')
        if len(v.strip()) < 3:
            raise ValueError('Slug должен содержать минимум 3 символа')
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Slug может содержать только латиницу, цифры, дефис и подчёркивание')
        return v.strip().lower()
    
    class Config:
        from_attributes = True


class CategoryCreate(BaseModelSchema):
    title: str = Field(max_length=256)
    description: str
    slug: str = Field(
        pattern=r'^[a-zA-Z0-9_-]+$',
        description="Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание."
    )
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Название категории не может быть пустым')
        if len(v.strip()) < 3:
            raise ValueError('Название категории должно содержать минимум 3 символа')
        return v.strip()
    
    @field_validator('description')
    @classmethod
    def validate_description(cls, v: str) -> str:
        """Валидация описания категории"""
        if not v or not v.strip():
            raise ValueError('Описание категории не может быть пустым')
        if len(v.strip()) < 3:
            raise ValueError('Описание должно содержать минимум 3 символа')
        return v.strip()
    
    @field_validator('slug')
    @classmethod
    def validate_slug(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Slug не может быть пустым')
        if len(v.strip()) < 3:
            raise ValueError('Slug должен содержать минимум 3 символа')
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Slug может содержать только латиницу, цифры, дефис и подчёркивание')
        return v.strip().lower()


class CategoryUpdate(BaseModelSchema):
    title: Optional[str] = Field(None, max_length=256)
    description: Optional[str] = None
    slug: Optional[str] = Field(
        None, 
        pattern=r'^[a-zA-Z0-9_-]+$'
    )
    is_published: Optional[bool] = None
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.strip():
                raise ValueError('Название категории не может быть пустым')
            if len(v.strip()) < 3:
                raise ValueError('Название категории должно содержать минимум 3 символа')
            return v.strip()
        return v
    
    @field_validator('description')
    @classmethod
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.strip():
                raise ValueError('Описание категории не может быть пустым')
            if len(v.strip()) < 2:
                raise ValueError('Описание категории должно содержать минимум 2 символов')
            return v.strip()
        return v
    
    @field_validator('slug')
    @classmethod
    def validate_slug(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.strip():
                raise ValueError('Slug не может быть пустым')
            if len(v.strip()) < 3:
                raise ValueError('Slug должен содержать минимум 3 символа')
            if not re.match(r'^[a-zA-Z0-9_-]+$', v):
                raise ValueError('Slug может содержать только латиницу, цифры, дефис и подчёркивание')
            return v.strip().lower()
        return v