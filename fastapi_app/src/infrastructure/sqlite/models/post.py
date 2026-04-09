from src.infrastructure.sqlite.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Boolean, DateTime, ForeignKey, Integer
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi_app.src.infrastructure.sqlite.models.users import User
    from fastapi_app.src.infrastructure.sqlite.models.category import Category
    from fastapi_app.src.infrastructure.sqlite.models.location import Location
    from fastapi_app.src.infrastructure.sqlite.models.comment import Comment

class Post(Base):
    __tablename__ = "blog_post"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    pub_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    image: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    author_id: Mapped[int] = mapped_column(ForeignKey("auth_user.id"), nullable=False)
    location_id: Mapped[Optional[int]] = mapped_column(ForeignKey("blog_location.id"), nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("blog_category.id"), nullable=False)
    
    author: Mapped["User"] = relationship("User", back_populates="posts")
    category: Mapped["Category"] = relationship("Category", back_populates="posts")
    location: Mapped[Optional["Location"]] = relationship("Location", back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    