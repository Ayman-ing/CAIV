# Development Guide

## Overview

This guide provides instructions for developers working on the AI Resume Builder project. It covers development workflows, coding standards, testing practices, and deployment procedures.

## Development Environment Setup

### Prerequisites

- **Python 3.12+**: Required for FastAPI and modern Python features
- **PostgreSQL 12+**: Database for production and development
- **UV Package Manager**: For dependency management and virtual environments
- **Git**: Version control
- **Docker** (optional): For containerized development

### Initial Setup

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd AIResumeBuilder/CAIV
   ```

2. **Install UV Package Manager**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Create Virtual Environment and Install Dependencies**
   ```bash
   uv sync
   ```

4. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database Setup**
   ```bash
   # Create PostgreSQL database
   createdb ai_resume_builder
   
   # Run migrations
   cd app
   uv run alembic upgrade head
   ```

6. **Start Development Server**
   ```bash
   uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## Project Structure

### Feature-Based Architecture

The project follows a feature-based architecture where each feature is self-contained:

```
features/
├── users/
│   ├── __init__.py
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── repository.py    # Data access layer
│   ├── service.py       # Business logic layer
│   └── router.py        # FastAPI routes
├── profiles/
│   ├── models.py
│   ├── schemas.py
│   ├── repository.py
│   ├── service.py
│   ├── router.py
│   └── education/       # Sub-features
│       ├── models.py
│       ├── schemas.py
│       ├── repository.py
│       ├── service.py
│       └── router.py
```

### Layer Responsibilities

1. **Models Layer** (`models.py`)
   - SQLAlchemy database models
   - Database relationships
   - Table definitions

2. **Schemas Layer** (`schemas.py`)
   - Pydantic models for API request/response
   - Data validation
   - Serialization/deserialization

3. **Repository Layer** (`repository.py`)
   - Database operations (CRUD)
   - Query optimization
   - Data access abstraction

4. **Service Layer** (`service.py`)
   - Business logic
   - Cross-feature operations
   - Data transformation

5. **Router Layer** (`router.py`)
   - HTTP route definitions
   - Request/response handling
   - Dependency injection

## Coding Standards

### Python Code Style

- **PEP 8**: Follow Python style guidelines
- **Type Hints**: Use type annotations for all functions
- **Docstrings**: Document all public functions and classes
- **Import Organization**: Use isort for import sorting

Example:

```python
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import HTTPException

from .models import User
from .schemas import UserCreate, UserResponse


class UserRepository:
    """Repository for user data operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, user_data: UserCreate) -> User:
        """Create a new user.
        
        Args:
            user_data: User creation data
            
        Returns:
            Created user instance
            
        Raises:
            HTTPException: If user creation fails
        """
        # Implementation here
        pass
```

### Database Conventions

1. **Table Names**: Use snake_case plural nouns
2. **Column Names**: Use snake_case
3. **Foreign Keys**: Format as `{table}_id`
4. **UUIDs**: Include UUID field for external access
5. **Timestamps**: Include created_at and updated_at

### API Conventions

1. **Endpoints**: Use RESTful URL patterns
2. **HTTP Methods**: GET, POST, PUT, DELETE
3. **Response Format**: Consistent JSON structure
4. **Error Handling**: Standardized error responses
5. **Status Codes**: Use appropriate HTTP status codes

## Development Workflow

### Feature Development

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/new-feature-name
   ```

2. **Implement Feature**
   - Start with models and schemas
   - Implement repository layer
   - Add service layer logic
   - Create router endpoints
   - Write tests

3. **Database Migrations**
   ```bash
   # Generate migration
   uv run alembic revision --autogenerate -m "Add new feature tables"
   
   # Apply migration
   uv run alembic upgrade head
   ```

4. **Testing**
   ```bash
   # Run tests
   uv run pytest
   
   # Run with coverage
   uv run pytest --cov=app
   ```

5. **Code Quality**
   ```bash
   # Format code
   uv run black .
   uv run isort .
   
   # Lint code
   uv run flake8 .
   uv run mypy .
   ```

### Git Workflow

1. **Commit Messages**: Use conventional commit format
   ```
   feat: add user profile management
   fix: resolve database connection issue
   docs: update API documentation
   test: add unit tests for user service
   ```

2. **Pull Requests**
   - Create descriptive PR titles
   - Include summary of changes
   - Link related issues
   - Ensure tests pass

3. **Code Review**
   - Review for code quality
   - Check test coverage
   - Verify documentation updates
   - Test functionality

## Testing Strategy

### Test Structure

```
tests/
├── conftest.py          # Test configuration
├── test_models.py       # Model tests
├── test_repositories.py # Repository tests
├── test_services.py     # Service tests
├── test_routers.py      # API endpoint tests
└── fixtures/            # Test data fixtures
```

### Testing Patterns

1. **Unit Tests**: Test individual functions/methods
2. **Integration Tests**: Test feature interactions
3. **API Tests**: Test HTTP endpoints
4. **Database Tests**: Test database operations

### Test Examples

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from features.users.models import User
from features.users.schemas import UserCreate


class TestUserAPI:
    """Test user API endpoints."""
    
    def test_create_user(self, client: TestClient, db: Session):
        """Test user creation endpoint."""
        user_data = {
            "email": "test@example.com",
            "location": "New York, NY",
            "phone_number": "+1-555-0123"
        }
        
        response = client.post("/api/v1/users", json=user_data)
        
        assert response.status_code == 201
        assert response.json()["data"]["email"] == user_data["email"]
        
        # Verify database record
        user = db.query(User).filter(User.email == user_data["email"]).first()
        assert user is not None
```

## Database Development

### Migration Best Practices

1. **Descriptive Names**: Use clear migration descriptions
2. **Reversible**: Ensure migrations can be rolled back
3. **Data Migrations**: Handle data transformations carefully
4. **Testing**: Test migrations on sample data

### Common Migration Patterns

```python
# Add new table
def upgrade():
    op.create_table(
        'new_table',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

# Add column
def upgrade():
    op.add_column('existing_table', sa.Column('new_column', sa.String()))

# Add index
def upgrade():
    op.create_index('idx_table_column', 'table_name', ['column_name'])
```

### Database Testing

1. **Test Database**: Use separate test database
2. **Fixtures**: Create reusable test data
3. **Cleanup**: Reset database state between tests
4. **Performance**: Test query performance with realistic data

## Performance Optimization

### Database Optimization

1. **Indexing**: Add indexes for frequently queried columns
2. **Query Optimization**: Use efficient queries
3. **Connection Pooling**: Configure connection pools
4. **Lazy Loading**: Use appropriate loading strategies

### API Optimization

1. **Pagination**: Implement pagination for large datasets
2. **Caching**: Cache frequently accessed data
3. **Rate Limiting**: Implement rate limiting
4. **Compression**: Use response compression

### Monitoring

1. **Logging**: Implement structured logging
2. **Metrics**: Track API performance metrics
3. **Error Tracking**: Monitor and track errors
4. **Database Monitoring**: Monitor database performance

## Security Guidelines

### Authentication & Authorization

1. **JWT Tokens**: Use secure token-based authentication
2. **Role-Based Access**: Implement role-based permissions
3. **Input Validation**: Validate all user inputs
4. **SQL Injection**: Use parameterized queries

### Data Protection

1. **UUID Usage**: Use UUIDs for external identifiers
2. **Sensitive Data**: Encrypt sensitive information
3. **Password Security**: Hash passwords securely
4. **Data Validation**: Validate all data inputs

### API Security

1. **HTTPS**: Use HTTPS in production
2. **CORS**: Configure CORS properly
3. **Rate Limiting**: Prevent abuse with rate limiting
4. **Input Sanitization**: Sanitize user inputs

## Deployment

### Environment Configuration

1. **Environment Variables**: Use environment variables for configuration
2. **Secrets Management**: Secure secret management
3. **Configuration Validation**: Validate configuration on startup

### Database Deployment

1. **Migration Strategy**: Plan migration deployments
2. **Backup Strategy**: Regular database backups
3. **Rollback Plan**: Have rollback procedures
4. **Performance Monitoring**: Monitor database performance

### Application Deployment

1. **Container Deployment**: Use Docker containers
2. **Health Checks**: Implement health check endpoints
3. **Graceful Shutdown**: Handle shutdown gracefully
4. **Load Balancing**: Configure load balancing

## AI Development

### Vector Embeddings

1. **Model Selection**: Choose appropriate embedding models
2. **Vector Storage**: Use Qdrant for vector storage
3. **Similarity Search**: Implement efficient similarity search
4. **Batch Processing**: Process embeddings in batches

### Resume Generation

1. **Template System**: Create flexible resume templates
2. **Content Optimization**: Optimize content for ATS systems
3. **Quality Assurance**: Validate generated content
4. **Performance**: Optimize generation speed

## Documentation

### Code Documentation

1. **Docstrings**: Document all public APIs
2. **Type Hints**: Use comprehensive type annotations
3. **Comments**: Add comments for complex logic
4. **Examples**: Provide usage examples

### API Documentation

1. **OpenAPI**: Maintain OpenAPI specifications
2. **Examples**: Provide request/response examples
3. **Error Codes**: Document error codes and messages
4. **Versioning**: Document API versioning strategy

## Troubleshooting

### Common Issues

1. **Database Connection**: Check connection settings
2. **Migration Errors**: Verify migration scripts
3. **Import Errors**: Check Python path and imports
4. **Performance Issues**: Profile and optimize queries

### Debug Tools

1. **Logging**: Use appropriate log levels
2. **Debugger**: Use Python debugger for complex issues
3. **Database Tools**: Use database administration tools
4. **Profiling**: Profile performance bottlenecks

### Support Resources

1. **Documentation**: Check project documentation
2. **Issue Tracker**: Use GitHub issues for bug reports
3. **Team Communication**: Use team chat for quick questions
4. **Code Review**: Request code reviews for complex changes
