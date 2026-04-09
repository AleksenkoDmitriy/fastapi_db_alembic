from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional


class BaseModelSchema(BaseModel):
    is_published: bool = Field(
        True, 
        description="Опубликовано. Снимите галочку, чтобы скрыть публикацию."
    )
    created_at: datetime = Field(default_factory=datetime.now)


class Location(BaseModelSchema):
    id: Optional[int] = None
    name: str = Field(max_length=256)
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Название локации не может быть пустым')
        if len(v.strip()) > 100:
            raise ValueError('Название локации не может превышать 100 символов')
        return v.strip()
    
    class Config:
        from_attributes = True


class LocationCreate(BaseModelSchema):
    name: str = Field(max_length=256)
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Название локации не может быть пустым')
        if len(v.strip()) > 100:
            raise ValueError('Название локации не может превышать 100 символов')
        return v.strip()


class LocationUpdate(BaseModelSchema):
    name: Optional[str] = Field(None, max_length=256)
    is_published: Optional[bool] = None
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.strip():
                raise ValueError('Название локации не может быть пустым')
            if len(v.strip()) > 100:
                raise ValueError('Название локации не может превышать 100 символов')
            return v.strip()
        return v