from src.infrastructure.sqlite.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, DateTime, ForeignKey, Integer
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi_app.src.infrastructure.sqlite.models.post import Post
    from fastapi_app.src.infrastructure.sqlite.models.users import User

class Comment(Base):
    __tablename__ = "blog_comment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    post_id: Mapped[int] = mapped_column(ForeignKey("blog_post.id"), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("auth_user.id"), nullable=False)
    
    post: Mapped["Post"] = relationship("Post", back_populates="comments")
    author: Mapped["User"] = relationship("User", back_populates="comments")