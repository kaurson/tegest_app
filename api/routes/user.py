from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlalchemy.orm import Session

from api.models import User, UserCreate, UserResponse, UserUpdate
from api.services.user_sqlalchemy_service import UserSQLAlchemyService
from database.database import get_db
from app.logger import logger

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user in the database
    """
    try:
        # Create service instance with database session
        user_service = UserSQLAlchemyService(db)
        
        # Check if email already exists
        existing_user = await user_service.get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        
        # Create new user in database
        new_user = await user_service.create_user(user)
        
        logger.info(f"New user registered: {new_user.email}")
        return new_user
        
    except HTTPException:
        raise
    except ValueError as e:
        # Handle database constraint errors
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during user registration"
        )

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    limit: int = 100, 
    offset: int = 0, 
    db: Session = Depends(get_db)
):
    """
    Get all registered users from database with pagination
    """
    try:
        user_service = UserSQLAlchemyService(db)
        users = await user_service.get_all_users(limit=limit, offset=offset)
        return users
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while fetching users"
        )

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: str, db: Session = Depends(get_db)):
    """
    Get user by ID from database
    """
    try:
        user_service = UserSQLAlchemyService(db)
        user = await user_service.get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while fetching user"
        )

@router.get("/users/email/{email}", response_model=UserResponse)
async def get_user_by_email(email: str, db: Session = Depends(get_db)):
    """
    Get user by email from database
    """
    try:
        user_service = UserSQLAlchemyService(db)
        user = await user_service.get_user_by_email(email)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching user by email {email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while fetching user"
        )

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user_update: UserUpdate, db: Session = Depends(get_db)):
    """
    Update user information in database
    """
    try:
        user_service = UserSQLAlchemyService(db)
        updated_user = await user_service.update_user(user_id, user_update)
        
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        logger.info(f"User updated: {user_id}")
        return updated_user
        
    except HTTPException:
        raise
    except ValueError as e:
        # Handle database constraint errors (email/username conflicts)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while updating user"
        )

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    """
    Delete user by ID from database
    """
    try:
        user_service = UserSQLAlchemyService(db)
        deleted = await user_service.delete_user(user_id)
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        logger.info(f"User deleted: {user_id}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while deleting user"
        )

@router.get("/users/search/{search_term}", response_model=List[UserResponse])
async def search_users(search_term: str, limit: int = 50, db: Session = Depends(get_db)):
    """
    Search users by name or email in database
    """
    try:
        user_service = UserSQLAlchemyService(db)
        # Use the proper search method from the service
        users = await user_service.search_users(search_term, limit=limit)
        return users
        
    except Exception as e:
        logger.error(f"Error searching users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while searching users"
        )
