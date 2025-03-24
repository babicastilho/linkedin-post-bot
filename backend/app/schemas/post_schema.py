from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class PostBase(BaseModel):
    """Base schema for creating and updating posts"""
    title: str = Field(..., example="Example Post Title")
    content: str = Field(..., example="This is an example post content.")
    status: str = Field("backlog", example="backlog")

class PostCreate(PostBase):
    """Schema for creating a new post"""
    pass  # Inherits all fields from PostBase

class PostUpdateStatus(BaseModel):
    """Schema for updating post status"""
    status: str = Field(..., example="scheduled")

class PostResponse(PostBase):
    """Schema for returning post data with datetime formatted as ISO 8601"""
    id: Optional[str] = Field(None, alias="_id")
    created_at: Optional[str] = None  # Converted to ISO format when returning
    updated_at: Optional[str] = None  # Converted to ISO format when returning

    class Config:
        orm_mode = True

    @staticmethod
    def convert_datetime(dt: Optional[datetime]) -> Optional[str]:
        """Ensures datetime fields are returned as ISO 8601 strings"""
        return dt.isoformat() if isinstance(dt, datetime) else None
