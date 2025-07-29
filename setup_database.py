#!/usr/bin/env python3
"""
Database setup script for Alembic migrations
This script helps set up the database environment and create initial migrations
"""

import os
import sys
from dotenv import load_dotenv, find_dotenv

def setup_database_env():
    """Set up database environment variables"""
    load_dotenv(find_dotenv())
    
    print("🔧 Database Setup Configuration")
    print("=" * 50)
    
    # Check if we have Supabase configuration
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if supabase_url and supabase_key:
        print("✅ Supabase configuration found")
        
        # For Supabase, we need to construct the database URL
        # Supabase uses a specific format for direct database connections
        if "supabase.co" in supabase_url:
            # Extract project reference from Supabase URL
            project_ref = supabase_url.split("//")[1].split(".")[0]
            
            # Supabase database connection format
            # You'll need to get these from your Supabase dashboard under Settings > Database
            print(f"📝 For Supabase project: {project_ref}")
            print("\nTo connect to your Supabase database directly, you need:")
            print("1. Go to your Supabase Dashboard > Settings > Database")
            print("2. Copy the connection string under 'Connection string' tab")
            print("3. Set it as DATABASE_URL in your .env file")
            print("\nExample format:")
            print(f"DATABASE_URL=postgresql://postgres:[PASSWORD]@db.{project_ref}.supabase.co:5432/postgres")
            
    # Check for regular database configuration
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        print(f"✅ DATABASE_URL found: {database_url[:50]}...")
        return True
    
    # Check for individual database components
    db_components = {
        "DB_HOST": os.getenv("DB_HOST"),
        "DB_PORT": os.getenv("DB_PORT", "5432"),
        "DB_NAME": os.getenv("DB_NAME", "postgres"),
        "DB_USER": os.getenv("DB_USER"),
        "DB_PASSWORD": os.getenv("DB_PASSWORD")
    }
    
    missing_components = [k for k, v in db_components.items() if not v and k != "DB_PASSWORD"]
    
    if missing_components:
        print("⚠️  Missing database configuration:")
        for component in missing_components:
            print(f"   - {component}")
        print("\nPlease add these to your .env file or set DATABASE_URL")
        return False
    
    # Construct DATABASE_URL from components
    constructed_url = f"postgresql://{db_components['DB_USER']}:{db_components['DB_PASSWORD']}@{db_components['DB_HOST']}:{db_components['DB_PORT']}/{db_components['DB_NAME']}"
    print(f"✅ Database URL constructed from components")
    return True

def create_migration_commands():
    """Display commands to create and run migrations"""
    print("\n🚀 Next Steps - Alembic Migration Commands")
    print("=" * 50)
    print("1. Create initial migration:")
    print("   alembic revision --autogenerate -m 'Initial migration - create users table'")
    print("\n2. Run migration:")
    print("   alembic upgrade head")
    print("\n3. Create future migrations:")
    print("   alembic revision --autogenerate -m 'Description of changes'")
    print("\n4. Check migration status:")
    print("   alembic current")
    print("\n5. View migration history:")
    print("   alembic history")
    print("\n6. Downgrade if needed:")
    print("   alembic downgrade -1")

def main():
    """Main setup function"""
    print("🏗️  Alembic Database Migration Setup")
    print("=" * 50)
    
    # Check if alembic is initialized
    if not os.path.exists("alembic"):
        print("❌ Alembic not initialized. Run: alembic init alembic")
        return
    
    if not os.path.exists("alembic.ini"):
        print("❌ alembic.ini not found. Run: alembic init alembic")
        return
    
    print("✅ Alembic configuration found")
    
    # Setup database environment
    if setup_database_env():
        print("\n✅ Database configuration ready")
    else:
        print("\n❌ Database configuration incomplete")
        return
    
    # Check if models are importable
    try:
        from database.models import User, Base
        print("✅ Database models imported successfully")
        print(f"📋 Found models: {[table.name for table in Base.metadata.tables.values()]}")
    except ImportError as e:
        print(f"❌ Could not import database models: {e}")
        return
    
    # Display next steps
    create_migration_commands()
    
    print("\n💡 Tips:")
    print("- Always review generated migrations before running them")
    print("- Test migrations on a copy of your data first")
    print("- Keep migrations small and focused")
    print("- Add descriptive messages to your migrations")

if __name__ == "__main__":
    main() 