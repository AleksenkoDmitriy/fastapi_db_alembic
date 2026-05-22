from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from src.schemas.users import User


class FollowResponse(BaseModel):
    follower_id: int
    following_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class FollowersResponse(BaseModel):
    user_id: int
    username: str
    email: str
    followed_at: datetime
    
    class Config:
        from_attributes = True


class FollowingResponse(BaseModel):
    user_id: int
    username: str
    email: str
    followed_at: datetime
    
    class Config:
        from_attributes = True


class SubscriptionStats(BaseModel):
    followers_count: int
    following_count: int
    is_following: bool = False