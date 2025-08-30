"""
Unit tests for UserService
"""
import pytest
from uuid import uuid4

from features.users.service import UserService
from features.users.schemas import UserCreate, UserUpdate
from features.users.models import User, UserRole


class TestUserService:
    """Test cases for UserService methods"""

    @pytest.fixture
    def user_service(self, db_session):
        """Create a UserService instance for testing"""
        return UserService(db_session)

    @pytest.fixture
    def sample_user_create(self):
        """Sample user creation data"""
        return UserCreate(
            email="test@example.com",
            password="TestPassword123!",
            confirm_password="TestPassword123!",
            first_name="Test",
            last_name="User"
        )

    @pytest.fixture
    def created_user(self, db_session, sample_user_create):
        """Create a user using AuthService for testing"""
        from features.auth.service import AuthService
        from features.auth.schemas import UserRegister
        
        auth_service = AuthService(db_session)
        user_register = UserRegister(**sample_user_create.model_dump())
        user, access_token = auth_service.register_user(user_register)
        return user

    # Note: Removed test_create_user_success since user creation should be done through AuthService

    def test_get_user_by_id_success(self, user_service, created_user):
        """Test getting user by ID"""
        retrieved_user = user_service.get_user(created_user.id)
        
        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.email == created_user.email

    def test_get_user_by_id_not_found(self, user_service):
        """Test getting non-existent user by ID"""
        user = user_service.get_user(99999)
        
        assert user is None

    def test_get_user_by_uuid_success(self, user_service, created_user):
        """Test getting user by UUID"""
        retrieved_user = user_service.get_user_by_uuid(str(created_user.uuid))
        
        assert retrieved_user is not None
        assert retrieved_user.uuid == created_user.uuid
        assert retrieved_user.email == created_user.email

    def test_get_user_by_uuid_not_found(self, user_service):
        """Test getting non-existent user by UUID"""
        fake_uuid = str(uuid4())
        user = user_service.get_user_by_uuid(fake_uuid)
        
        assert user is None

    def test_get_user_by_email_success(self, user_service, created_user):
        """Test getting user by email"""
        retrieved_user = user_service.get_user_by_email(created_user.email)
        
        assert retrieved_user is not None
        assert retrieved_user.email == created_user.email
        assert retrieved_user.id == created_user.id

    def test_get_user_by_email_not_found(self, user_service):
        """Test getting non-existent user by email"""
        user = user_service.get_user_by_email("nonexistent@example.com")
        
        assert user is None

    def test_list_users_empty(self, user_service):
        """Test listing users when none exist"""
        users = user_service.list_users()
        
        assert users == []

    def test_list_users_with_data(self, user_service, created_user):
        """Test listing users with existing data"""
        users = user_service.list_users()
        
        assert len(users) >= 1
        assert any(user.email == created_user.email for user in users)

    def test_list_users_pagination(self, user_service, db_session):
        """Test user listing with pagination"""
        from features.auth.service import AuthService
        from features.auth.schemas import UserRegister
        
        auth_service = AuthService(db_session)
        
        # Create multiple users
        for i in range(5):
            user_register = UserRegister(
                email=f"user{i}@example.com",
                password="Password123!",
                confirm_password="Password123!",
                first_name=f"User{i}",
                last_name="Test"
            )
            auth_service.register_user(user_register)
        
        # Test pagination
        users_page1 = user_service.list_users(skip=0, limit=2)
        users_page2 = user_service.list_users(skip=2, limit=2)
        
        assert len(users_page1) == 2
        assert len(users_page2) == 2
        assert users_page1[0].id != users_page2[0].id

    def test_update_user_success(self, user_service, created_user):
        """Test successful user update"""
        update_data = UserUpdate(
            first_name="Updated",
            last_name="Name",
            email="updated@example.com"
        )
        
        updated_user = user_service.update_user(created_user.id, update_data)
        
        assert updated_user is not None
        assert updated_user.first_name == "Updated"
        assert updated_user.last_name == "Name"
        assert updated_user.email == "updated@example.com"
        assert updated_user.id == created_user.id

    def test_update_user_not_found(self, user_service):
        """Test updating non-existent user"""
        update_data = UserUpdate(first_name="Updated")
        
        updated_user = user_service.update_user(99999, update_data)
        
        assert updated_user is None

    def test_update_user_by_uuid_success(self, user_service, created_user):
        """Test successful user update by UUID"""        
        update_data = UserUpdate(
            first_name="UUIDUpdated",
            last_name="Name"
        )
        
        updated_user = user_service.update_user_by_uuid(str(created_user.uuid), update_data)
        
        assert updated_user is not None
        assert updated_user.first_name == "UUIDUpdated"
        assert updated_user.last_name == "Name"
        assert updated_user.uuid == created_user.uuid

    def test_update_user_by_uuid_not_found(self, user_service):
        """Test updating non-existent user by UUID"""
        fake_uuid = str(uuid4())
        update_data = UserUpdate(first_name="Updated")
        
        updated_user = user_service.update_user_by_uuid(fake_uuid, update_data)
        
        assert updated_user is None

    def test_delete_user_by_uuid_success(self, user_service, created_user):
        """Test successful user deletion by UUID"""        
        result = user_service.delete_user_by_uuid(str(created_user.uuid))
        
        assert result is True
        
        # Verify user is deleted
        deleted_user = user_service.get_user_by_uuid(str(created_user.uuid))
        assert deleted_user is None

    def test_delete_user_by_uuid_not_found(self, user_service):
        """Test deleting non-existent user by UUID"""
        fake_uuid = str(uuid4())
        
        result = user_service.delete_user_by_uuid(fake_uuid)
        
        assert result is False

    def test_partial_update(self, user_service, created_user):
        """Test partial user update (only some fields)"""        
        # Update only first name
        update_data = UserUpdate(first_name="PartialUpdate")
        
        updated_user = user_service.update_user(created_user.id, update_data)
        
        assert updated_user is not None
        assert updated_user.first_name == "PartialUpdate"
        assert updated_user.last_name == created_user.last_name  # Should remain unchanged
        assert updated_user.email == created_user.email  # Should remain unchanged

    def test_user_service_consistency(self, user_service, created_user):
        """Test that different access methods return consistent data"""        
        # Get user by different methods
        user_by_id = user_service.get_user(created_user.id)
        user_by_uuid = user_service.get_user_by_uuid(str(created_user.uuid))
        user_by_email = user_service.get_user_by_email(created_user.email)
        
        # All should return the same user data
        assert user_by_id.id == user_by_uuid.id == user_by_email.id
        assert user_by_id.uuid == user_by_uuid.uuid == user_by_email.uuid
        assert user_by_id.email == user_by_uuid.email == user_by_email.email


class TestUserServiceIntegration:
    """Integration tests for UserService with different scenarios"""

    @pytest.fixture
    def user_service(self, db_session):
        """Create a UserService instance for testing"""
        return UserService(db_session)

    # Note: Removed test_create_multiple_users_different_emails since user creation should be done through AuthService
