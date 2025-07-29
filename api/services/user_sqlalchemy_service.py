from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from datetime import datetime
from fastapi import Depends

from models import UserDB as UserModel
from database.database import get_db
from models import UserCreate, UserResponse, UserUpdate
from app.logger import logger

class UserSQLAlchemyService:
    """Service layer for user database operations using SQLAlchemy ORM"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """Create a new user in the database using SQLAlchemy"""
        try:
            # Extract first name from full name
            first_name = user_data.full_name.split()[0] if user_data.full_name else ""
            
            # Create SQLAlchemy model instance
            db_user = UserModel(
                first_name=first_name,
                full_name=user_data.full_name,
                username=user_data.username,
                email=user_data.email,
                password=user_data.password  # Note: In production, hash this password!
            )
            
            # Add to session and commit
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            
            logger.info(f"User created successfully: {db_user.email}")
            
            # Convert to response model
            return UserResponse(
                id=str(db_user.id),
                first_name=db_user.first_name,
                username=db_user.username,
                email=db_user.email,
                full_name=db_user.full_name,
                created_at=db_user.created_at,
                updated_at=db_user.updated_at
            )
            
        except IntegrityError as e:
            self.db.rollback()
            if "email" in str(e.orig):
                raise ValueError("Email already exists")
            elif "username" in str(e.orig):
                raise ValueError("Username already exists")
            else:
                raise ValueError(f"Database integrity error: {str(e)}")
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating user: {str(e)}")
            raise Exception(f"Failed to create user: {str(e)}")
    
    async def get_user_by_id(self, user_id: str) -> Optional[UserResponse]:
        """Get user by ID using SQLAlchemy"""
        try:
            db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
            
            if db_user:
                return UserResponse(
                    id=str(db_user.id),
                    first_name=db_user.first_name,
                    username=db_user.username,
                    email=db_user.email,
                    full_name=db_user.full_name,
                    created_at=db_user.created_at,
                    updated_at=db_user.updated_at
                )
            return None
            
        except Exception as e:
            logger.error(f"Error fetching user {user_id}: {str(e)}")
            raise Exception(f"Failed to fetch user: {str(e)}")
    
    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """Get user by email using SQLAlchemy"""
        try:
            db_user = self.db.query(UserModel).filter(UserModel.email == email).first()
            
            if db_user:
                return UserResponse(
                    id=str(db_user.id),
                    first_name=db_user.first_name,
                    username=db_user.username,
                    email=db_user.email,
                    full_name=db_user.full_name,
                    created_at=db_user.created_at,
                    updated_at=db_user.updated_at
                )
            return None
            
        except Exception as e:
            logger.error(f"Error fetching user by email {email}: {str(e)}")
            raise Exception(f"Failed to fetch user by email: {str(e)}")
    
    async def get_all_users(self, limit: int = 100, offset: int = 0) -> List[UserResponse]:
        """Get all users with pagination using SQLAlchemy"""
        try:
            db_users = (self.db.query(UserModel)
                       .offset(offset)
                       .limit(limit)
                       .all())
            
            return [
                UserResponse(
                    id=str(user.id),
                    first_name=user.first_name,
                    username=user.username,
                    email=user.email,
                    full_name=user.full_name,
                    created_at=user.created_at,
                    updated_at=user.updated_at
                )
                for user in db_users
            ]
            
        except Exception as e:
            logger.error(f"Error fetching all users: {str(e)}")
            raise Exception(f"Failed to fetch users: {str(e)}")
    
    async def search_users(self, search_term: str, limit: int = 50) -> List[UserResponse]:
        """Search users by name or email using database-level search"""
        try:
            # Use SQLAlchemy's ilike for case-insensitive search
            db_users = (self.db.query(UserModel)
                       .filter(
                           or_(
                               UserModel.first_name.ilike(f"%{search_term}%"),
                               UserModel.full_name.ilike(f"%{search_term}%"),
                               UserModel.email.ilike(f"%{search_term}%")
                           )
                       )
                       .limit(limit)
                       .all())
            
            return [
                UserResponse(
                    id=str(user.id),
                    first_name=user.first_name,
                    username=user.username,
                    email=user.email,
                    full_name=user.full_name,
                    created_at=user.created_at,
                    updated_at=user.updated_at
                )
                for user in db_users
            ]
            
        except Exception as e:
            logger.error(f"Error searching users: {str(e)}")
            raise Exception(f"Failed to search users: {str(e)}")
    
    async def update_user(self, user_id: str, user_update: UserUpdate) -> Optional[UserResponse]:
        """Update user information using SQLAlchemy"""
        try:
            db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
            
            if not db_user:
                return None
            
            # Update fields that are provided
            if user_update.first_name is not None:
                db_user.first_name = user_update.first_name
            if user_update.full_name is not None:
                db_user.full_name = user_update.full_name
                # If full_name is provided, extract first name from it
                db_user.first_name = user_update.full_name.split()[0] if user_update.full_name else db_user.first_name
            if user_update.username is not None:
                db_user.username = user_update.username
            if user_update.email is not None:
                db_user.email = user_update.email
            if user_update.password is not None:
                db_user.password = user_update.password  # Note: In production, hash this password!
            
            # Commit changes
            self.db.commit()
            self.db.refresh(db_user)
            
            logger.info(f"User updated successfully: {user_id}")
            
            return UserResponse(
                id=str(db_user.id),
                first_name=db_user.first_name,
                username=db_user.username,
                email=db_user.email,
                full_name=db_user.full_name,
                created_at=db_user.created_at,
                updated_at=db_user.updated_at
            )
            
        except IntegrityError as e:
            self.db.rollback()
            if "email" in str(e.orig):
                raise ValueError("Email already exists")
            elif "username" in str(e.orig):
                raise ValueError("Username already exists")
            else:
                raise ValueError(f"Database integrity error: {str(e)}")
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating user {user_id}: {str(e)}")
            raise Exception(f"Failed to update user: {str(e)}")
    
    async def delete_user(self, user_id: str) -> bool:
        """Delete user by ID using SQLAlchemy"""
        try:
            db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
            
            if not db_user:
                return False
            
            self.db.delete(db_user)
            self.db.commit()
            
            logger.info(f"User deleted successfully: {user_id}")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting user {user_id}: {str(e)}")
            raise Exception(f"Failed to delete user: {str(e)}")

# Dependency function for FastAPI - this should be synchronous
def get_user_service(db: Session = Depends(get_db)) -> UserSQLAlchemyService:
    """Get UserService instance with database session"""
    return UserSQLAlchemyService(db) 