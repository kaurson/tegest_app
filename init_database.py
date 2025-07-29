#!/usr/bin/env python3
"""
Database initialization script
Creates database tables and runs initial setup
"""

import os
import sys
from dotenv import load_dotenv, find_dotenv

def check_environment():
    """Check if environment is properly configured"""
    load_dotenv(find_dotenv())
    
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        print("Please add DATABASE_URL to your .env file")
        print("\nExample for Supabase:")
        print("DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres")
        return False
    
    print(f"✅ DATABASE_URL found: {database_url[:50]}...")
    return True

def test_imports():
    """Test that all required modules can be imported"""
    try:
        from database.models import User, Base
        from database.database import engine, SessionLocal
        print("✅ Database models and configuration imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import database modules: {e}")
        return False

def create_tables_with_sqlalchemy():
    """Create tables using SQLAlchemy (without Alembic)"""
    try:
        from database.models import Base
        from database.database import engine
        
        print("🏗️  Creating database tables with SQLAlchemy...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    try:
        from database.database import SessionLocal
        
        print("🔗 Testing database connection...")
        db = SessionLocal()
        
        # Try a simple query
        result = db.execute("SELECT 1").scalar()
        db.close()
        
        if result == 1:
            print("✅ Database connection successful")
            return True
        else:
            print("❌ Database connection test failed")
            return False
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def create_sample_user():
    """Create a sample user for testing"""
    try:
        from database.database import SessionLocal
        from database.models import User
        import uuid
        
        print("👤 Creating sample user...")
        db = SessionLocal()
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == "test@example.com").first()
        if existing_user:
            print("ℹ️  Sample user already exists")
            db.close()
            return True
        
        # Create sample user
        sample_user = User(
            id=uuid.uuid4(),
            first_name="Test User",
            username="testuser",
            email="test@example.com"
        )
        
        db.add(sample_user)
        db.commit()
        db.refresh(sample_user)
        db.close()
        
        print(f"✅ Sample user created: {sample_user.email}")
        return True
    except Exception as e:
        print(f"❌ Failed to create sample user: {e}")
        return False

def run_alembic_migrations():
    """Run Alembic migrations if available"""
    try:
        import subprocess
        
        print("🔄 Running Alembic migrations...")
        
        # Check if any migrations exist
        if not os.path.exists("alembic/versions") or not os.listdir("alembic/versions"):
            print("ℹ️  No Alembic migrations found. Creating initial migration...")
            
            # Create initial migration
            result = subprocess.run([
                "alembic", "revision", "--autogenerate", 
                "-m", "Initial migration - create users table"
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ Failed to create migration: {result.stderr}")
                return False
            
            print("✅ Initial migration created")
        
        # Run migrations
        result = subprocess.run(["alembic", "upgrade", "head"], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Alembic migrations completed successfully")
            return True
        else:
            print(f"❌ Alembic migration failed: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("⚠️  Alembic not found. Using SQLAlchemy table creation instead.")
        return create_tables_with_sqlalchemy()
    except Exception as e:
        print(f"❌ Failed to run migrations: {e}")
        return False

def main():
    """Main initialization function"""
    print("🚀 Database Initialization")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        return False
    
    # Test imports
    if not test_imports():
        return False
    
    # Test database connection
    if not test_database_connection():
        return False
    
    # Try Alembic first, fallback to SQLAlchemy
    if not run_alembic_migrations():
        print("⚠️  Alembic setup failed, trying direct SQLAlchemy table creation...")
        if not create_tables_with_sqlalchemy():
            return False
    
    # Create sample user
    create_sample_user()  # This is optional, so we don't fail if it doesn't work
    
    print("\n🎉 Database initialization completed!")
    print("\nNext steps:")
    print("1. Start your FastAPI application: python3 run.py")
    print("2. Test the user registration endpoint at /register")
    print("3. View API documentation at http://localhost:8000/docs")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 