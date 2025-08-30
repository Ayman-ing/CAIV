"""
Unit tests for AuthService
"""
import pytest
from datetime import datetime, timedelta
from core.exceptions import HTTPException
import jwt
import os

from features.auth.service import AuthService
from features.auth.schemas import UserRegister, PasswordChange
from features.users.models import User


class TestAuthService:
    """Test cases for AuthService methods"""

    def test_password_hashing(self):
        """Test password hashing and verification"""
        password = "test_password_123"
        
        # Test hashing
        hashed = AuthService.get_password_hash(password)
        assert isinstance(hashed, str)
        assert len(hashed) > 0
        assert hashed != password  # Should be different from original
        
        # Test verification
        assert AuthService.verify_password(password, hashed) is True
        assert AuthService.verify_password("wrong_password", hashed) is False

    def test_create_access_token(self):
        """Test JWT token creation"""
        data = {"sub": "test@example.com", "user_id": "123"}
        
        # Test with default expiration
        token = AuthService.create_access_token(data)
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Decode and verify token
        secret_key = "test_secret_key_for_testing_only"  # Same as in conftest.py
        decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
        assert decoded["sub"] == "test@example.com"
        assert decoded["user_id"] == "123"
        assert "exp" in decoded
        assert "iat" in decoded
        
        # Test with custom expiration
        custom_delta = timedelta(minutes=60)
        token_custom = AuthService.create_access_token(data, expires_delta=custom_delta)
        assert isinstance(token_custom, str)
        assert len(token_custom) > 0

    def test_create_access_token_with_enhanced_payload(self):
        """Test JWT token creation with enhanced payload (name and role)"""
        data = {
            "sub": "123e4567-e89b-12d3-a456-426614174000",
            "name": "John Doe", 
            "role": "admin"
        }
        
        # Create token
        token = AuthService.create_access_token(data)
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Decode and verify enhanced payload
        secret_key = "test_secret_key_for_testing_only"
        decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
        
        # Verify all fields are present
        assert decoded["sub"] == "123e4567-e89b-12d3-a456-426614174000"
        assert decoded["name"] == "John Doe"
        assert decoded["role"] == "admin"
        assert "exp" in decoded
        assert "iat" in decoded

    def test_verify_token_valid(self):
        """Test verifying valid JWT token"""
        data = {"sub": "test@example.com"}
        token = AuthService.create_access_token(data)

        decoded_data = AuthService.verify_token(token)
        assert decoded_data["sub"] == "test@example.com"
        assert "exp" in decoded_data
        assert "iat" in decoded_data

    def test_verify_token_invalid(self):
        """Test verifying invalid JWT token"""
        # Test with completely invalid token
        with pytest.raises(HTTPException) as exc_info:
            AuthService.verify_token("invalid_token")
        assert exc_info.value.status_code == 401

        # Test with expired token (create manually expired token)
        past_time = datetime.utcnow() - timedelta(hours=1)
        expired_data = {"sub": "test@example.com", "exp": past_time.timestamp()}
        secret_key = "test_secret_key_for_testing_only"
        expired_token = jwt.encode(expired_data, secret_key, algorithm="HS256")
        
        with pytest.raises(HTTPException) as exc_info:
            AuthService.verify_token(expired_token)
        assert exc_info.value.status_code == 401

    def test_register_user_success(self, auth_service, sample_user_data):
        """Test successful user registration"""
        user_register = UserRegister(**sample_user_data)
        
        user, access_token = auth_service.register_user(user_register)
        
        # Verify user object
        assert isinstance(user, User)
        assert user.email == sample_user_data["email"]
        assert user.is_active is True
        assert user.uuid is not None
        
        # Verify access token
        assert isinstance(access_token, str)
        assert len(access_token) > 0
        
        # Verify token can be decoded
        decoded_data = AuthService.verify_token(access_token)
        assert decoded_data["sub"] == str(user.uuid)

    def test_register_user_duplicate_email(self, auth_service, sample_user_data, created_user):
        """Test registration with duplicate email"""
        user_register = UserRegister(**sample_user_data)
        
        with pytest.raises(HTTPException) as exc_info:
            auth_service.register_user(user_register)
        
        assert exc_info.value.status_code == 400
        assert "already registered" in exc_info.value.message.lower()

    def test_authenticate_user_success(self, auth_service, sample_user_data, created_user):
        """Test successful user authentication"""
        user, access_token = auth_service.authenticate_user(
            sample_user_data["email"], 
            sample_user_data["password"]
        )
        
        assert isinstance(user, User)
        assert user.email == sample_user_data["email"]
        assert user.uuid == created_user.uuid
        
        assert isinstance(access_token, str)
        assert len(access_token) > 0

    def test_authenticate_user_wrong_email(self, auth_service, sample_user_data, created_user):
        """Test authentication with wrong email"""
        with pytest.raises(HTTPException) as exc_info:
            auth_service.authenticate_user("wrong@example.com", sample_user_data["password"])
        
        assert exc_info.value.status_code == 401
        assert "incorrect" in exc_info.value.message.lower()

    def test_authenticate_user_wrong_password(self, auth_service, sample_user_data, created_user):
        """Test authentication with wrong password"""
        with pytest.raises(HTTPException) as exc_info:
            auth_service.authenticate_user(sample_user_data["email"], "wrong_password")
        
        assert exc_info.value.status_code == 401
        assert "incorrect" in exc_info.value.message.lower()

    def test_change_password_success(self, auth_service, created_user, sample_user_data):
        """Test successful password change"""
        password_change = PasswordChange(
            current_password=sample_user_data["password"],
            new_password="NewPassword123!",
            confirm_new_password="NewPassword123!"
        )
        
        # Should not raise exception
        auth_service.change_user_password(created_user, password_change)
        
        # Verify old password no longer works
        with pytest.raises(HTTPException):
            auth_service.authenticate_user(created_user.email, sample_user_data["password"])
        
        # Verify new password works
        user, token = auth_service.authenticate_user(created_user.email, "NewPassword123!")
        assert user.uuid == created_user.uuid

    def test_change_password_wrong_current_password(self, auth_service, created_user):
        """Test password change with wrong current password"""
        password_change = PasswordChange(
            current_password="wrong_password",
            new_password="NewPassword123!",
            confirm_new_password="NewPassword123!"
        )
        
        with pytest.raises(HTTPException) as exc_info:
            auth_service.change_user_password(created_user, password_change)
        
        assert exc_info.value.status_code == 400
        assert "incorrect" in exc_info.value.message.lower()


class TestPasswordValidation:
    """Test password validation logic"""

    def test_password_strength_validation(self):
        """Test password strength requirements"""
        # This test depends on your password validation rules
        # For now, just test basic hashing functionality
        weak_password = "123"
        strong_password = "SecurePassword123!"
        
        # Both should hash successfully (validation is in Pydantic models)
        weak_hash = AuthService.get_password_hash(weak_password)
        strong_hash = AuthService.get_password_hash(strong_password)
        
        assert len(weak_hash) > 0
        assert len(strong_hash) > 0
        assert weak_hash != strong_hash
