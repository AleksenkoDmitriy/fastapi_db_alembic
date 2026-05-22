from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from src.infrastructure.postgres.database import Base

class Subscription(Base):
    __tablename__ = "blog_subscription"
    __table_args__ = (
        UniqueConstraint('follower_id', 'following_id', name='unique_follow'),
        {'extend_existing': True}
    )
    
    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("auth_user.id", ondelete="CASCADE"), nullable=False)
    following_id = Column(Integer, ForeignKey("auth_user.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
