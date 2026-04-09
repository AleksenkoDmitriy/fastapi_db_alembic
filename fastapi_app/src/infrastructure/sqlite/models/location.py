from src.infrastructure.sqlite.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, DateTime, Integer
from datetime import datetime
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi_app.src.infrastructure.sqlite.models.post import Post

class Location(Base):
    __tablename__ = "blog_location"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    new: Mapped[int] = mapped_column(Integer, nullable=True)
    
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="location")