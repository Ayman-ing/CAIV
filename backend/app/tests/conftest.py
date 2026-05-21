"""
Test configuration and fixtures for the auth module tests
"""
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
import sys
from typing import AsyncGenerator

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set test environment variables
os.environ["JWT_SECRET"] = "test_secret_key_for_testing_only"

from main import app
from db.session import get_db
from shared.models.registry import Base
from features.users.models import User
from features.auth.service import AuthService


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
)
AsyncTestingSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


@pytest.fixture(scope="function")
async def db_session():
    """Create a test database session"""
    # Create tables
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    async with AsyncTestingSessionLocal() as session:
        yield session

    # Drop tables after test
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def client(db_session):
    """Create a test client with database dependency override"""
    async def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as test_client:
        yield test_client

    # Clean up overrides
    app.dependency_overrides.clear()


@pytest.fixture
async def auth_service(db_session):
    """Create an AuthService instance for testing"""
    return AuthService(db_session)


@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "email": "test@example.com",
        "password": "TestPassword123!",
        "confirm_password": "TestPassword123!",
        "first_name": "Test",
        "last_name": "User"
    }


@pytest.fixture
async def created_user(db_session, auth_service, sample_user_data):
    """Create a user in the database for testing"""
    from features.auth.schemas import UserRegister

    user_register = UserRegister(**sample_user_data)
    user, token = await auth_service.register_user(user_register)
    return user


@pytest.fixture
def auth_headers(created_user, auth_service):
    """Create authentication headers for testing protected endpoints"""
    token = auth_service.create_access_token(data={
        "sub": str(created_user.uuid),
        "role": created_user.role.value
    })
    return {"Authorization": f"Bearer {token}"}


# Test environment variables
@pytest.fixture(autouse=True)
def setup_test_env():
    """Set up test environment variables"""
    original_env = os.environ.copy()

    # Set test environment variables
    os.environ["JWT_SECRET"] = "test_secret_key_for_testing_only"
    os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"

    yield

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)
