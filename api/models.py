from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class User(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50, description="User's first name")
    username: str = Field(..., min_length=3, max_length=30, description="Unique username")
    email: EmailStr = Field(..., description="User's email address")
    
    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "username": "johndoe",
                "email": "john.doe@example.com"
            }
        }

class UserCreate(BaseModel):
    """Model for creating a new user"""
    full_name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    username: str = Field(..., min_length=3, max_length=30, description="Unique username")
    email: EmailStr = Field(..., description="User's email address")
    
    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "John Doe",
                "username": "johndoe",
                "email": "john.doe@example.com"
            }
        }

class UserResponse(BaseModel):
    """Model for user response (excludes sensitive data)"""
    id: Optional[str] = None
    first_name: str
    username: str
    email: EmailStr
    full_name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UserUpdate(BaseModel):
    """Model for updating user information"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    username: Optional[str] = Field(None, min_length=3, max_length=30)
    email: Optional[EmailStr] = None
