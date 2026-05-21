from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Like(Base):
    __tablename__ = "blog_like"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("blog_post.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("auth_user.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    post = relationship("Post", back_populates="likes")
    user = relationship("User", back_populates="likes")
    
    __table_args__ = (
        UniqueConstraint('post_id', 'user_id', name='unique_post_user_like'),
    )