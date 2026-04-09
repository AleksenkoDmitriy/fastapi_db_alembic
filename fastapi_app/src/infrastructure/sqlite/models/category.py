from src.infrastructure.sqlite.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Boolean, DateTime, Integer
from datetime import datetime
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi_app.src.infrastructure.sqlite.models.post import Post

class Category(Base):
    __tablename__ = "blog_category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(256))
    description: Mapped[str] = mapped_column(Text)
    slug: Mapped[str] = mapped_column(String(50), unique=True)
    is_published: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="category")