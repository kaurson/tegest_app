# Combined Models File (NOT RECOMMENDED for production)
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import Column, String, Integer, DateTime, Text, ARRAY, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from typing import Optional
from datetime import datetime
import uuid

# SQLAlchemy Base
Base = declarative_base()

# ============================================================================
# SQLAlchemy Database Models (for Alembic and database operations)
# ============================================================================

class UserDB(Base):
    """SQLAlchemy User model for database schema management"""
    __tablename__ = "users"
    
    # Primary key - UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    
    # Basic user information
    first_name = Column(String(50), nullable=False)
    full_name = Column(String(100), nullable=False)
    username = Column(String(30), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
    
    def to_dict(self):
        """Convert SQLAlchemy model to dictionary"""
        return {
            'id': str(self.id),
            'first_name': self.first_name,
            'full_name': self.full_name,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

# ============================================================================
# Pydantic API Models (for FastAPI validation and serialization)
# ============================================================================

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
    password: str = Field(..., min_length=8, max_length=128, description="User's password")
    
    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "John Doe",
                "username": "johndoe",
                "email": "john.doe@example.com",
                "password": "securepassword123"
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
    password: Optional[str] = Field(None, min_length=8, max_length=128, description="New password") 