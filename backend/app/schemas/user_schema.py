from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserBase(BaseModel):
    """Base schema for user"""
    username: Optional[str] = Field(default=None, example="john_doe")
    email: EmailStr = Field(..., example="johndoe@example.com")

class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., example="securepassword123")

class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str

class UserResponse(UserBase):
    """Schema for returning user data"""
    id: Optional[str] = Field(default=None, alias="_id")
    created_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
        "json_encoders": {
            datetime: lambda v: v.isoformat()
        }
    }
