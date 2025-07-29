# Database Migration Setup with Alembic

This directory contains the database models and migration configuration for the application using Alembic with SQLAlchemy.

## 🏗️ **Setup Overview**

- **SQLAlchemy Models**: `database/models.py` - Database schema definitions
- **Database Config**: `database/database.py` - Connection and session management
- **Alembic Config**: `alembic/` - Migration scripts and configuration
- **Setup Script**: `setup_database.py` - Helper script for configuration

## 📦 **Dependencies**

The following packages are required (already added to `requirements.txt`):
```
alembic>=1.16.4
sqlalchemy>=2.0.32
psycopg2-binary>=2.9.10
```

## 🔧 **Configuration**

### Environment Variables

Add to your `.env` file:

#### Option 1: Direct Database URL (Recommended)
```env
DATABASE_URL=postgresql://username:password@host:port/database_name
```

#### Option 2: For Supabase
```env
# Get this from Supabase Dashboard > Settings > Database > Connection string
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres
```

#### Option 3: Individual Components
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password
```

## 🚀 **Getting Started**

### 1. Check Configuration
```bash
python3 setup_database.py
```

### 2. Create Initial Migration
```bash
alembic revision --autogenerate -m "Initial migration - create users table"
```

### 3. Apply Migration
```bash
alembic upgrade head
```

## 📋 **Common Alembic Commands**

### Migration Management
```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Apply specific migration
alembic upgrade [revision_id]

# Downgrade one step
alembic downgrade -1

# Downgrade to specific revision
alembic downgrade [revision_id]
```

### Status and History
```bash
# Check current migration status
alembic current

# View migration history
alembic history

# Show verbose history
alembic history --verbose
```

### Advanced Operations
```bash
# Create empty migration (for manual changes)
alembic revision -m "Custom changes"

# Show SQL without executing
alembic upgrade head --sql

# Merge multiple heads (if needed)
alembic merge [revision1] [revision2] -m "Merge migrations"
```

## 🏛️ **Database Models**

### Current Models

#### User Model (`database/models.py`)
```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(50), nullable=False)
    username = Column(String(30), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```

### Adding New Models

1. Define model in `database/models.py`
2. Import in `database/__init__.py` if needed
3. Create migration: `alembic revision --autogenerate -m "Add new model"`
4. Review generated migration file
5. Apply: `alembic upgrade head`

## 🔄 **Integration with FastAPI**

### Using SQLAlchemy Service

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from database.database import get_db
from api.services.user_sqlalchemy_service import UserSQLAlchemyService

@router.post("/users")
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    service = UserSQLAlchemyService(db)
    return await service.create_user(user_data)
```

### Database Session Management

The `get_db()` function provides a database session for each request:
- Automatic connection management
- Transaction rollback on errors
- Connection cleanup after request

## 🔍 **Troubleshooting**

### Common Issues

#### 1. Import Errors
```bash
# Ensure you're in the project root and models are importable
python3 -c "from database.models import User; print('Models imported successfully')"
```

#### 2. Database Connection Issues
```bash
# Test database connection
python3 -c "from database.database import engine; print(engine.execute('SELECT 1').scalar())"
```

#### 3. Migration Conflicts
```bash
# If you have multiple heads, merge them
alembic merge [head1] [head2] -m "Merge conflicting migrations"
```

#### 4. Reset Migrations (Development Only)
```bash
# Drop all tables and recreate
alembic downgrade base
alembic upgrade head
```

### Environment Issues

1. **DATABASE_URL not found**: Check your `.env` file
2. **Permission denied**: Verify database user permissions
3. **Connection timeout**: Check database host and port
4. **SSL issues**: Add `?sslmode=require` to your DATABASE_URL for cloud databases

## 📚 **Best Practices**

### Migration Best Practices
- Always review generated migrations before applying
- Test migrations on a copy of production data
- Keep migrations small and focused
- Use descriptive migration messages
- Never edit applied migrations

### Model Development
- Use proper column constraints
- Add indexes for frequently queried columns
- Use appropriate data types
- Consider foreign key relationships
- Add helpful `__repr__` methods

### Production Deployment
- Backup database before migrations
- Test migrations in staging environment
- Use `--sql` flag to review SQL before execution
- Consider downtime requirements for large table changes

## 🆘 **Support**

If you encounter issues:
1. Run `python3 setup_database.py` to verify configuration
2. Check the Alembic logs for detailed error messages
3. Verify your database connection and permissions
4. Review the migration files in `alembic/versions/` 