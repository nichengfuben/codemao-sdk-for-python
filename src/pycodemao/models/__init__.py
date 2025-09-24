"""Pydantic models for CodeMao API responses."""

from datetime import datetime
from typing import Optional, List, Dict, Any, Union
from uuid import UUID
from pydantic import BaseModel, Field, validator, HttpUrl


class BaseCodeMaoModel(BaseModel):
    """Base model with common configuration."""
    
    class Config:
        extra = "allow"
        validate_assignment = True
        use_enum_values = True


class User(BaseCodeMaoModel):
    """User model representing a CodeMao user."""
    
    id: UUID = Field(..., description="User unique identifier")
    username: str = Field(..., description="Username")
    nickname: str = Field(..., description="Display name")
    email: Optional[str] = Field(None, description="Email address")
    avatar: Optional[HttpUrl] = Field(None, description="Avatar URL")
    bio: Optional[str] = Field(None, description="User biography")
    level: int = Field(1, ge=1, description="User level")
    exp: int = Field(0, ge=0, description="Experience points")
    coins: int = Field(0, ge=0, description="Coins balance")
    diamonds: int = Field(0, ge=0, description="Diamonds balance")
    followers_count: int = Field(0, ge=0, description="Number of followers")
    following_count: int = Field(0, ge=0, description="Number of following")
    works_count: int = Field(0, ge=0, description="Number of works")
    posts_count: int = Field(0, ge=0, description="Number of posts")
    created_at: datetime = Field(..., description="Account creation time")
    last_login_at: Optional[datetime] = Field(None, description="Last login time")
    is_verified: bool = Field(False, description="Verified account status")
    is_premium: bool = Field(False, description="Premium membership status")
    
    @validator('username')
    def validate_username(cls, v: str) -> str:
        if len(v) < 3 or len(v) > 20:
            raise ValueError('Username must be between 3 and 20 characters')
        if not v.replace('_', '').isalnum():
            raise ValueError('Username can only contain letters, numbers, and underscores')
        return v
    
    @validator('nickname')
    def validate_nickname(cls, v: str) -> str:
        if len(v) > 50:
            raise ValueError('Nickname cannot exceed 50 characters')
        return v


class Work(BaseCodeMaoModel):
    """Work model representing a user's creation."""
    
    id: UUID = Field(..., description="Work unique identifier")
    title: str = Field(..., description="Work title")
    description: Optional[str] = Field(None, description="Work description")
    author: User = Field(..., description="Work author")
    thumbnail: Optional[HttpUrl] = Field(None, description="Thumbnail URL")
    content: Optional[str] = Field(None, description="Work content/code")
    language: Optional[str] = Field(None, description="Programming language")
    tags: List[str] = Field(default_factory=list, description="Work tags")
    likes_count: int = Field(0, ge=0, description="Number of likes")
    comments_count: int = Field(0, ge=0, description="Number of comments")
    collections_count: int = Field(0, ge=0, description="Number of collections")
    views_count: int = Field(0, ge=0, description="Number of views")
    is_public: bool = Field(True, description="Public visibility")
    is_featured: bool = Field(False, description="Featured work status")
    created_at: datetime = Field(..., description="Creation time")
    updated_at: Optional[datetime] = Field(None, description="Last update time")
    
    @validator('title')
    def validate_title(cls, v: str) -> str:
        if len(v) < 1 or len(v) > 100:
            raise ValueError('Title must be between 1 and 100 characters')
        return v


class Post(BaseCodeMaoModel):
    """Post model representing a forum post."""
    
    id: UUID = Field(..., description="Post unique identifier")
    title: str = Field(..., description="Post title")
    content: str = Field(..., description="Post content")
    author: User = Field(..., description="Post author")
    board: 'ForumBoard' = Field(..., description="Forum board")
    is_pinned: bool = Field(False, description="Pinned post status")
    is_locked: bool = Field(False, description="Locked post status")
    likes_count: int = Field(0, ge=0, description="Number of likes")
    comments_count: int = Field(0, ge=0, description="Number of comments")
    views_count: int = Field(0, ge=0, description="Number of views")
    tags: List[str] = Field(default_factory=list, description="Post tags")
    created_at: datetime = Field(..., description="Creation time")
    updated_at: Optional[datetime] = Field(None, description="Last update time")
    
    @validator('title')
    def validate_title(cls, v: str) -> str:
        if len(v) < 1 or len(v) > 200:
            raise ValueError('Title must be between 1 and 200 characters')
        return v
    
    @validator('content')
    def validate_content(cls, v: str) -> str:
        if len(v) < 1 or len(v) > 10000:
            raise ValueError('Content must be between 1 and 10000 characters')
        return v


class ForumBoard(BaseCodeMaoModel):
    """Forum board model."""
    
    id: UUID = Field(..., description="Board unique identifier")
    name: str = Field(..., description="Board name")
    description: Optional[str] = Field(None, description="Board description")
    category: str = Field(..., description="Board category")
    posts_count: int = Field(0, ge=0, description="Number of posts")
    moderators: List[User] = Field(default_factory=list, description="Board moderators")
    is_active: bool = Field(True, description="Board active status")
    created_at: datetime = Field(..., description="Creation time")
    
    @validator('name')
    def validate_name(cls, v: str) -> str:
        if len(v) < 1 or len(v) > 50:
            raise ValueError('Board name must be between 1 and 50 characters')
        return v


class APIResponse(BaseCodeMaoModel):
    """Standard API response wrapper."""
    
    success: bool = Field(..., description="Request success status")
    code: int = Field(..., description="Response code")
    message: str = Field(..., description="Response message")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    
    
class PaginatedResponse(BaseCodeMaoModel):
    """Paginated response wrapper."""
    
    items: List[Dict[str, Any]] = Field(..., description="List of items")
    total: int = Field(..., ge=0, description="Total number of items")
    page: int = Field(..., ge=1, description="Current page number")
    per_page: int = Field(..., ge=1, description="Items per page")
    total_pages: int = Field(..., ge=0, description="Total number of pages")
    has_next: bool = Field(..., description="Has next page")
    has_prev: bool = Field(..., description="Has previous page")