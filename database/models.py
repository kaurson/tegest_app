from sqlalchemy import Column, String, Integer, DateTime, Text, ARRAY, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class User(Base):
    """SQLAlchemy User model for database schema management"""
    __tablename__ = "users"
    
    # Primary key - UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    
    # Basic user information
    first_name = Column(String(50), nullable=True)
    full_name = Column(String(100), nullable=True)
    username = Column(String(30), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=True)
    
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