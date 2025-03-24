from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class PostBase(BaseModel):
    """Base schema for creating and updating posts"""
    title: str = Field(..., example="Example Post Title")
    content: str = Field(..., example="This is an example post content.")
    status: str = Field(default="backlog", example="backlog")

class PostCreate(PostBase):
    """Schema for creating a new post"""
    pass

class PostUpdateStatus(BaseModel):
    """Schema for updating post status"""
    status: str = Field(..., example="scheduled")

class PostResponse(PostBase):
    """Schema for returning post data with datetime formatted as ISO 8601"""
    id: Optional[str] = Field(default=None, alias="_id")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
        "json_encoders": {
            datetime: lambda v: v.isoformat()
        }
    }
