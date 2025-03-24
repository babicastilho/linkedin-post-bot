from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    """Base schema for user"""
    username: str = Field(..., example="john_doe")
    email: EmailStr = Field(..., example="johndoe@example.com")

class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., example="securepassword123")

class UserResponse(UserBase):
    """Schema for returning user data"""
    id: Optional[str] = Field(None, alias="_id")

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str
