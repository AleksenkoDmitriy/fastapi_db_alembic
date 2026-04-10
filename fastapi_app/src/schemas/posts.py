from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from src.schemas.users import User
from src.schemas.category import Category
from src.schemas.location import Location


class BaseModelSchema(BaseModel):
    is_published: bool = Field(
        True,
        description="Опубликовано. Снимите галочку, чтобы скрыть публикацию."
    )
    created_at: datetime = Field(default_factory=datetime.now)


class Post(BaseModelSchema):
    id: Optional[int] = None
    title: str = Field(max_length=256)
    text: str
    pub_date: datetime = Field(
        description="Если установить дату и время в будущем — можно делать отложенные публикации."
    )
    author: User
    location: Optional[Location] = None
    category: Category
    image: Optional[str] = Field(None, description="URL изображения")

    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Заголовок поста не может быть пустым')
        if len(v.strip()) < 5:
            raise ValueError('Заголовок поста должен содержать минимум 5 символов')
        return v.strip()
    
    @field_validator('text')
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Текст поста не может быть пустым')
        if len(v.strip()) < 20:
            raise ValueError('Текст поста должен содержать минимум 20 символов')
        return v.strip()
    
    @field_validator('pub_date')
    @classmethod
    def validate_pub_date(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            v = v.replace(tzinfo=datetime.now().astimezone().tzinfo)
        return v

    @property
    def is_past_pub_date(self) -> bool:
        return self.pub_date <= datetime.now(self.pub_date.tzinfo)
    
    class Config:
        from_attributes = True


class PostCreate(BaseModelSchema):
    title: str = Field(max_length=256)
    text: str
    pub_date: datetime
    location_id: Optional[int] = None
    category_id: int
    image: Optional[str] = None
    is_published: bool = True
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Заголовок поста не может быть пустым')
        if len(v.strip()) < 5:
            raise ValueError('Заголовок поста должен содержать минимум 5 символов')
        return v.strip()
    
    @field_validator('text')
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Текст поста не может быть пустым')
        if len(v.strip()) < 20:
            raise ValueError('Текст поста должен содержать минимум 20 символов')
        return v.strip()
    
    @field_validator('category_id')
    @classmethod
    def validate_category_id(cls, v: int) -> int:
        if v <= 0:
            raise ValueError('ID категории должен быть положительным числом')
        return v
    
    @field_validator('location_id')
    @classmethod
    def validate_location_id(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v <= 0:
            raise ValueError('ID локации должен быть положительным числом')
        return v


class PostUpdate(BaseModelSchema):
    title: Optional[str] = Field(None, max_length=256)
    text: Optional[str] = None
    pub_date: Optional[datetime] = None
    location_id: Optional[int] = None
    category_id: Optional[int] = None
    image: Optional[str] = None
    is_published: Optional[bool] = None
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.strip():
                raise ValueError('Заголовок поста не может быть пустым')
            if len(v.strip()) < 5:
                raise ValueError('Заголовок поста должен содержать минимум 5 символов')
            return v.strip()
        return v
    
    @field_validator('text')
    @classmethod
    def validate_text(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.strip():
                raise ValueError('Текст поста не может быть пустым')
            if len(v.strip()) < 20:
                raise ValueError('Текст поста должен содержать минимум 20 символов')
            return v.strip()
        return v


class PostListResponse(BaseModel):
    id: int
    title: str
    text: str
    pub_date: datetime
    author_id: int
    category_id: int
    image: Optional[str] = None
    
    class Config:
        from_attributes = True