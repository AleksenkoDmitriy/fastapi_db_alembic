from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional
from datetime import datetime
import re


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=150)
    email: str = Field(...)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Имя пользователя не может быть пустым')
        if len(v.strip()) < 3:
            raise ValueError('Имя пользователя должно содержать минимум 3 символа')
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Имя пользователя может содержать только латиницу, цифры и подчёркивание')
        return v.strip().lower()



class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    is_superuser: bool = False
    is_staff: bool = False
    is_active: bool = True
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError('Пароль должен содержать минимум 6 символов')
        if not any(c.isupper() for c in v):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву')
        if not any(c.isdigit() for c in v):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')
        return v


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=150)
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=6)
    is_superuser: Optional[bool] = None
    is_staff: Optional[bool] = None
    is_active: Optional[bool] = None
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.strip():
                raise ValueError('Имя пользователя не может быть пустым')
            if not re.match(r'^[a-zA-Z0-9_]+$', v):
                raise ValueError('Имя пользователя может содержать только латиницу, цифры и подчёркивание')
            return v.strip().lower()
        return v
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.strip():
                raise ValueError('Email не может быть пустым')
            return v.strip().lower()
        return v
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if len(v) < 6:
                raise ValueError('Пароль должен содержать минимум 6 символов')
            if not any(c.isupper() for c in v):
                raise ValueError('Пароль должен содержать хотя бы одну заглавную букву')
            if not any(c.isdigit() for c in v):
                raise ValueError('Пароль должен содержать хотя бы одну цифру')
        return v


class User(UserBase):
    id: int
    is_superuser: bool
    is_staff: bool
    is_active: bool
    last_login: Optional[datetime] = None
    date_joined: Optional[datetime] = None
    
    class Config:
        from_attributes = True