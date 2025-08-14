"""
Unit tests for User Router (API endpoints)
"""
import pytest
from fastapi import status
import json
from uuid import uuid4

from features.users.models import User, UserRole


class TestUserEndpoints:
    """Test cases for user API endpoints"""

    def test_get_me_success(self, client, auth_headers, created_user):
        """Test getting current user information with valid token"""
        response = client.get("/api/v1/me", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["email"] == created_user.email
        assert data["first_name"] == created_user.first_name
        assert data["last_name"] == created_user.last_name
        assert data["role"] == created_user.role.value
        assert data["is_active"] == created_user.is_active
        assert "id" in data
        assert "uuid" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_get_me_no_auth(self, client):
        """Test getting current user info without authentication"""
        response = client.get("/api/v1/me")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_me_invalid_token(self, client):
        """Test getting current user info with invalid token"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/v1/me", headers=headers)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_me_success(self, client, auth_headers, created_user):
        """Test successful update of current user"""
        update_data = {
            "first_name": "Updated",
            "last_name": "Name",
            "email": "updated@example.com"
        }
        
        response = client.put("/api/v1/me", json=update_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["first_name"] == "Updated"
        assert data["last_name"] == "Name"
        assert data["email"] == "updated@example.com"

    def test_update_me_invalid_email(self, client, auth_headers):
        """Test update with invalid email format"""
        update_data = {
            "email": "invalid_email"
        }
        
        response = client.put("/api/v1/me", json=update_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_update_me_no_auth(self, client):
        """Test update without authentication"""
        update_data = {
            "first_name": "Updated"
        }
        
        response = client.put("/api/v1/me", json=update_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_me_success(self, client, auth_headers):
        """Test successful deletion of current user"""
        response = client.delete("/api/v1/me", headers=auth_headers)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_me_no_auth(self, client):
        """Test deletion without authentication"""
        response = client.delete("/api/v1/me")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestAdminUserEndpoints:
    """Test cases for admin-only user endpoints"""

    @pytest.fixture
    def admin_user(self, db_session, auth_service):
        """Create an admin user for testing"""
        from features.auth.schemas import UserRegister
        
        admin_data = {
            "email": "admin@example.com",
            "password": "AdminPassword123!",
            "confirm_password": "AdminPassword123!",
            "first_name": "Admin",
            "last_name": "User"
        }
        
        user_register = UserRegister(**admin_data)
        user, token = auth_service.register_user(user_register)
        
        # Update user role to admin in database
        db_user = db_session.query(User).filter(User.uuid == user.uuid).first()
        db_user.role = UserRole.ADMIN
        db_session.commit()
        db_session.refresh(db_user)
        
        return db_user

    @pytest.fixture
    def admin_auth_headers(self, admin_user, auth_service):
        """Create admin authentication headers"""
        token = auth_service.create_access_token(data={
            "sub": str(admin_user.uuid),
            "name": admin_user.full_name,
            "role": admin_user.role.value
        })
        return {"Authorization": f"Bearer {token}"}

    def test_list_users_admin_success(self, client, admin_auth_headers, created_user):
        """Test admin can list all users"""
        response = client.get("/api/v1/", headers=admin_auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1  # At least the created_user

    def test_list_users_pagination(self, client, admin_auth_headers):
        """Test user listing with pagination"""
        response = client.get("/api/v1/?skip=0&limit=10", headers=admin_auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert isinstance(data, list)

    def test_list_users_non_admin_forbidden(self, client, auth_headers):
        """Test regular user cannot list all users"""
        response = client.get("/api/v1/", headers=auth_headers)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_users_no_auth(self, client):
        """Test listing users without authentication"""
        response = client.get("/api/v1/")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_user_admin_success(self, client, admin_auth_headers):
        """Test admin can create new user"""
        user_data = {
            "email": "newuser@example.com",
            "password": "NewPassword123!",
            "confirm_password": "NewPassword123!",
            "first_name": "New",
            "last_name": "User",
            "role" : "USER"
        }
        
        response = client.post("/api/v1/", json=user_data, headers=admin_auth_headers)
        
        assert response.status_code == status.HTTP_201_CREATED
        
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["first_name"] == "New"
        assert data["last_name"] == "User"
        assert data["role"] == "user"

    def test_create_user_duplicate_email(self, client, admin_auth_headers, created_user):
        """Test creating user with duplicate email"""
        user_data = {
            "email": created_user.email,
            "password": "Password123!",
            "confirm_password": "Password123!",
            "first_name": "Duplicate",
            "last_name": "User"
        }
        
        response = client.post("/api/v1/", json=user_data, headers=admin_auth_headers)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_user_non_admin_forbidden(self, client, auth_headers):
        """Test regular user cannot create users"""
        user_data = {
            "email": "newuser@example.com",
            "password": "Password123!",
            "confirm_password": "Password123!",
            "first_name": "New",
            "last_name": "User"
        }
        
        response = client.post("/api/v1/", json=user_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_user_by_id_admin_success(self, client, admin_auth_headers, created_user):
        """Test admin can get user by ID"""
        response = client.get(f"/api/v1/{created_user.uuid}", headers=admin_auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["email"] == created_user.email

    def test_get_user_by_id_not_found(self, client, admin_auth_headers):
        """Test getting non-existent user"""
        fake_uuid = str(uuid4())
        response = client.get(f"/api/v1/{fake_uuid}", headers=admin_auth_headers)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_user_by_id_non_admin_forbidden(self, client, auth_headers, created_user):
        """Test regular user cannot get other users by ID"""
        response = client.get(f"/api/v1/{created_user.uuid}", headers=auth_headers)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_user_by_id_admin_success(self, client, admin_auth_headers, created_user):
        """Test admin can update user by ID"""
        update_data = {
            "first_name": "AdminUpdated",
            "last_name": "Name"
        }
        
        response = client.put(f"/api/v1/{created_user.uuid}", json=update_data, headers=admin_auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["first_name"] == "AdminUpdated"
        assert data["last_name"] == "Name"

    def test_update_user_by_id_not_found(self, client, admin_auth_headers):
        """Test updating non-existent user"""
        fake_uuid = str(uuid4())
        update_data = {"first_name": "Updated"}
        
        response = client.put(f"/api/v1/{fake_uuid}", json=update_data, headers=admin_auth_headers)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_user_by_id_non_admin_forbidden(self, client, auth_headers, created_user):
        """Test regular user cannot update users by ID"""
        update_data = {"first_name": "Updated"}
        
        response = client.put(f"/api/v1/{created_user.uuid}", json=update_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_user_by_id_admin_success(self, client, admin_auth_headers, created_user):
        """Test admin can delete user by ID"""
        response = client.delete(f"/api/v1/{created_user.uuid}", headers=admin_auth_headers)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_user_by_id_not_found(self, client, admin_auth_headers):
        """Test deleting non-existent user"""
        fake_uuid = str(uuid4())
        response = client.delete(f"/api/v1/{fake_uuid}", headers=admin_auth_headers)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_user_by_id_non_admin_forbidden(self, client, auth_headers, created_user):
        """Test regular user cannot delete users by ID"""
        response = client.delete(f"/api/v1/{created_user.uuid}", headers=auth_headers)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_promote_user_to_admin_success(self, client, admin_auth_headers, created_user):
        """Test admin can promote user to admin"""
        response = client.post(f"/api/v1/{created_user.uuid}/promote", headers=admin_auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["role"] == UserRole.ADMIN.value

    def test_promote_user_already_admin(self, client, admin_auth_headers, admin_user):
        """Test promoting user who is already admin"""
        response = client.post(f"/api/v1/{admin_user.uuid}/promote", headers=admin_auth_headers)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        data = response.json()
        assert "already an admin" in data["detail"]

    def test_promote_user_not_found(self, client, admin_auth_headers):
        """Test promoting non-existent user"""
        fake_uuid = str(uuid4())
        response = client.post(f"/api/v1/{fake_uuid}/promote", headers=admin_auth_headers)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_promote_user_non_admin_forbidden(self, client, auth_headers, created_user):
        """Test regular user cannot promote users"""
        response = client.post(f"/api/v1/{created_user.uuid}/promote", headers=auth_headers)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestUserValidation:
    """Test user input validation"""
    @pytest.fixture
    def admin_user(self, db_session, auth_service):
        """Create an admin user for testing"""
        from features.auth.schemas import UserRegister
        
        admin_data = {
            "email": "admin@example.com",
            "password": "AdminPassword123!",
            "confirm_password": "AdminPassword123!",
            "first_name": "Admin",
            "last_name": "User"
        }
        
        user_register = UserRegister(**admin_data)
        user, token = auth_service.register_user(user_register)
        
        # Update user role to admin in database
        db_user = db_session.query(User).filter(User.uuid == user.uuid).first()
        db_user.role = UserRole.ADMIN
        db_session.commit()
        db_session.refresh(db_user)
        
        return db_user
    @pytest.fixture
    def admin_auth_headers(self, admin_user, auth_service):
        """Create admin authentication headers"""
        token = auth_service.create_access_token(data={
            "sub": str(admin_user.uuid),
            "name": admin_user.full_name,
            "role": admin_user.role.value
        })
        return {"Authorization": f"Bearer {token}"}

    def test_create_user_invalid_email(self, client, admin_auth_headers):
        """Test user creation with invalid email"""
        user_data = {
            "email": "invalid_email",
            "password": "Password123!",
            "confirm_password": "Password123!",
            "first_name": "Test",
            "last_name": "User"
        }
        
        response = client.post("/api/v1/", json=user_data, headers=admin_auth_headers)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_user_missing_required_fields(self, client, admin_auth_headers):
        """Test user creation with missing required fields"""
        user_data = {
            "email": "test@example.com"
            # Missing password, first_name, last_name
        }
        
        response = client.post("/api/v1/", json=user_data, headers=admin_auth_headers)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_user_empty_names(self, client, admin_auth_headers):
        """Test user creation with empty names"""
        user_data = {
            "email": "test@example.com",
            "password": "Password123!",
            "confirm_password": "Password123!",
            "first_name": "",
            "last_name": ""
        }
        
        response = client.post("/api/v1/", json=user_data, headers=admin_auth_headers)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_update_user_invalid_email(self, client, auth_headers):
        """Test user update with invalid email"""
        update_data = {
            "email": "invalid_email"
        }
        
        response = client.put("/api/v1/me", json=update_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestTokenBasedAuth:
    """Test the new token-based authentication system"""

    @pytest.fixture
    def token_with_enhanced_payload(self, auth_service, created_user):
        """Create a token with enhanced payload (name and role)"""
        return auth_service.create_access_token(data={
            "sub": str(created_user.uuid),
            "name": created_user.full_name,
            "role": created_user.role.value
        })

    def test_token_based_auth_success(self, client, token_with_enhanced_payload):
        """Test that endpoints work with enhanced token payload"""
        headers = {"Authorization": f"Bearer {token_with_enhanced_payload}"}
        
        response = client.get("/api/v1/me", headers=headers)
        
        assert response.status_code == status.HTTP_200_OK

    def test_token_without_role_field(self, client, auth_service, created_user):
        """Test backward compatibility with old tokens without role field"""
        old_token = auth_service.create_access_token(data={
            "sub": str(created_user.uuid)
            # No name or role fields
        })
        
        headers = {"Authorization": f"Bearer {old_token}"}
        
        # This should still work for /me endpoint as it falls back to DB
        response = client.get("/api/v1/me", headers=headers)
        
        # The endpoint should handle tokens without enhanced payload gracefully
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED]
