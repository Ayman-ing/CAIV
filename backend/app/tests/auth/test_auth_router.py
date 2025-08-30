"""
Unit tests for Auth Router (API endpoints)
"""
import pytest
from fastapi import status
import json

from features.users.models import User


class TestAuthRouter:
    """Test cases for authentication API endpoints"""

    def test_register_success(self, client, sample_user_data):
        """Test successful user registration via API"""
        response = client.post("/api/v1/auth/register", json=sample_user_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert "expires_in" in data
        assert "user_id" in data
        
        assert data["token_type"] == "bearer"
        assert type(data["expires_in"]) == int
        assert isinstance(data["user_id"], str)
        assert len(data["access_token"]) > 0

    def test_register_duplicate_email(self, client, sample_user_data, created_user):
        """Test registration with duplicate email"""
        response = client.post("/api/v1/auth/register", json=sample_user_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert "already registered" in data["message"].lower()

    def test_register_invalid_email(self, client, sample_user_data):
        """Test registration with invalid email format"""
        invalid_data = sample_user_data.copy()
        invalid_data["email"] = "invalid_email"
        
        response = client.post("/api/v1/auth/register", json=invalid_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_missing_fields(self, client):
        """Test registration with missing required fields"""
        incomplete_data = {
            "email": "test@example.com"
            # Missing password, first_name, last_name
        }
        
        response = client.post("/api/v1/auth/register", json=incomplete_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_weak_password_too_short(self, client, sample_user_data):
        """Test registration with password too short (less than 8 characters)"""
        invalid_data = sample_user_data.copy()
        invalid_data["password"] = "Short1"  # 6 characters
        invalid_data["confirm_password"] = "Short1"
        
        response = client.post("/api/v1/auth/register", json=invalid_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        data = response.json()
        assert any("at least 8 characters" in str(error) for error in data["message"])

    def test_register_weak_password_no_uppercase(self, client, sample_user_data):
        """Test registration with password missing uppercase letter"""
        invalid_data = sample_user_data.copy()
        invalid_data["password"] = "lowercase123"
        invalid_data["confirm_password"] = "lowercase123"
        
        response = client.post("/api/v1/auth/register", json=invalid_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        data = response.json()
        assert any("uppercase letter" in str(error) for error in data["message"])

    def test_register_weak_password_no_lowercase(self, client, sample_user_data):
        """Test registration with password missing lowercase letter"""
        invalid_data = sample_user_data.copy()
        invalid_data["password"] = "UPPERCASE123"
        invalid_data["confirm_password"] = "UPPERCASE123"
        
        response = client.post("/api/v1/auth/register", json=invalid_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        data = response.json()
        assert any("lowercase letter" in str(error) for error in data["message"])

    def test_register_weak_password_no_number(self, client, sample_user_data):
        """Test registration with password missing number"""
        invalid_data = sample_user_data.copy()
        invalid_data["password"] = "NoNumbers"
        invalid_data["confirm_password"] = "NoNumbers"
        
        response = client.post("/api/v1/auth/register", json=invalid_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        data = response.json()
        assert any("number" in str(error) for error in data["message"])

    def test_register_strong_password_success(self, client, sample_user_data):
        """Test registration with strong password meeting all requirements"""
        valid_data = sample_user_data.copy()
        valid_data["email"] = "strongpass@example.com"  # Different email to avoid conflict
        valid_data["password"] = "StrongPass123"
        valid_data["confirm_password"] = "StrongPass123"
        
        response = client.post("/api/v1/auth/register", json=valid_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_success(self, client, sample_user_data, created_user):
        """Test successful login via API"""
        login_data = {
            "username": sample_user_data["email"],  # OAuth2PasswordRequestForm uses 'username'
            "password": sample_user_data["password"]
        }
        
        response = client.post("/api/v1/auth/login", data=login_data)
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert "expires_in" in data
        assert "user_id" in data
        
        assert data["token_type"] == "bearer"
        assert data["expires_in"] == 1800
        assert data["user_id"] == str(created_user.uuid)

    def test_login_wrong_email(self, client, sample_user_data, created_user):
        """Test login with wrong email"""
        login_data = {
            "username": "wrong@example.com",
            "password": sample_user_data["password"]
        }
        
        response = client.post("/api/v1/auth/login", data=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = response.json()
        assert "incorrect" in data["message"].lower()

    def test_login_wrong_password(self, client, sample_user_data, created_user):
        """Test login with wrong password"""
        login_data = {
            "username": sample_user_data["email"],
            "password": "wrong_password"
        }
        
        response = client.post("/api/v1/auth/login", data=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = response.json()
        assert "incorrect" in data["message"].lower()

    def test_login_missing_credentials(self, client):
        """Test login with missing credentials"""
        response = client.post("/api/v1/auth/login", data={})
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_me_success(self, client, auth_headers, created_user):
        """Test getting current user info with valid token"""
        response = client.get("/api/v1/me", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["email"] == created_user.email
        assert data["first_name"] == created_user.first_name
        assert data["last_name"] == created_user.last_name
        assert data["is_active"] == created_user.is_active

    def test_get_me_no_token(self, client):
        """Test getting current user info without token"""
        response = client.get("/api/v1/me")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_me_invalid_token(self, client):
        """Test getting current user info with invalid token"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/v1/me", headers=headers)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_change_password_success(self, client, auth_headers, sample_user_data):
        """Test successful password change via API"""
        change_data = {
            "current_password": sample_user_data["password"],
            "new_password": "NewPassword123!",
            "confirm_new_password": "NewPassword123!"
        }
        
        response = client.post("/api/v1/auth/change-password", 
                             json=change_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["message"] == "Password changed successfully"

    def test_change_password_wrong_current(self, client, auth_headers):
        """Test password change with wrong current password"""
        change_data = {
            "current_password": "wrong_password",
            "new_password": "NewPassword123!",
            "confirm_new_password": "NewPassword123!"
        }
        
        response = client.post("/api/v1/auth/change-password", 
                             json=change_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_change_password_no_auth(self, client):
        """Test password change without authentication"""
        change_data = {
            "current_password": "current_pass",
            "new_password": "NewPassword123!"
        }
        
        response = client.post("/api/v1/auth/change-password", json=change_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_logout_success(self, client, auth_headers):
        """Test successful logout via API"""
        response = client.post("/api/v1/auth/logout", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["message"] == "Successfully logged out"

    def test_logout_no_auth(self, client):
        """Test logout without authentication"""
        response = client.post("/api/v1/auth/logout")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestAuthRouterValidation:
    """Test input validation for auth endpoints"""

    def test_register_weak_password(self, client, sample_user_data):
        """Test registration with weak password"""
        weak_data = sample_user_data.copy()
        weak_data["password"] = "123"
        
        response = client.post("/api/v1/auth/register", json=weak_data)
        
        # This depends on your password validation rules
        # Adjust based on your implementation
        assert response.status_code in [status.HTTP_422_UNPROCESSABLE_ENTITY, status.HTTP_400_BAD_REQUEST]

    def test_register_invalid_email_formats(self, client, sample_user_data):
        """Test registration with various invalid email formats"""
        invalid_emails = [
            "not_an_email",
            "@example.com",
            "test@",
            "test.example.com",
            ""
        ]
        
        for invalid_email in invalid_emails:
            test_data = sample_user_data.copy()
            test_data["email"] = invalid_email
            
            response = client.post("/api/v1/auth/register", json=test_data)
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_long_names(self, client, sample_user_data):
        """Test registration with very long names"""
        long_data = sample_user_data.copy()
        long_data["first_name"] = "a" * 1000
        long_data["last_name"] = "b" * 1000
        
        response = client.post("/api/v1/auth/register", json=long_data)
        
        # This depends on your field length validation
        # Adjust based on your implementation
        assert response.status_code in [status.HTTP_422_UNPROCESSABLE_ENTITY, status.HTTP_400_BAD_REQUEST]


class TestAuthRouterSecurity:
    """Test security aspects of auth endpoints"""

    def test_password_not_returned_in_responses(self, client, sample_user_data):
        """Ensure passwords are never returned in API responses"""
        # Test registration
        response = client.post("/api/v1/auth/register", json=sample_user_data)
        data = response.json()
        
        # Check that password is not in response
        response_str = json.dumps(data)
        assert sample_user_data["password"] not in response_str
        assert "password" not in data

    def test_token_expiration_handling(self, client, auth_service, created_user):
        """Test handling of expired tokens"""
        from datetime import timedelta
        
        # Create an expired token
        expired_token = auth_service.create_access_token(
            data={"sub": created_user.email},
            expires_delta=timedelta(seconds=-1)
        )
        
        headers = {"Authorization": f"Bearer {expired_token}"}
        response = client.get("/api/v1/me", headers=headers)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_malformed_authorization_header(self, client):
        """Test various malformed authorization headers"""
        malformed_headers = [
            {"Authorization": "invalid"},
            {"Authorization": "Bearer"},
            {"Authorization": "Basic token"},
            {"Authorization": ""},
        ]
        
        for headers in malformed_headers:
            response = client.get("/api/v1/me", headers=headers)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
