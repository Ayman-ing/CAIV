"""
Tests for Role-Based Access Control (RBAC)
"""
import pytest
from core.exceptions import HTTPException
from unittest.mock import Mock

from core.rbac import admin_required, check_access, ensure_access, require_admin
from features.users.models import User, UserRole


class TestRBACFunctions:
    """Test RBAC utility functions"""
    
    def test_check_access_admin_user(self):
        """Admin can access any resource"""
        admin_user = Mock(spec=User)
        admin_user.is_admin = True
        admin_user.id = 1
        
        # Admin can access any user's resource
        assert check_access(admin_user, resource_user_id=999) == True
        assert check_access(admin_user, resource_user_id=1) == True
    
    def test_check_access_regular_user_own_resource(self):
        """Regular user can access their own resource"""
        regular_user = Mock(spec=User)
        regular_user.is_admin = False
        regular_user.id = 5
        
        # User can access their own resource
        assert check_access(regular_user, resource_user_id=5) == True
    
    def test_check_access_regular_user_other_resource(self):
        """Regular user cannot access other user's resource"""
        regular_user = Mock(spec=User)
        regular_user.is_admin = False
        regular_user.id = 5
        
        # User cannot access other user's resource
        assert check_access(regular_user, resource_user_id=999) == False
    
    def test_ensure_access_admin_success(self):
        """Admin access should not raise exception"""
        admin_user = Mock(spec=User)
        admin_user.is_admin = True
        admin_user.id = 1
        
        # Should not raise exception
        ensure_access(admin_user, resource_user_id=999, resource_name="profile")
    
    def test_ensure_access_owner_success(self):
        """Owner access should not raise exception"""
        user = Mock(spec=User)
        user.is_admin = False
        user.id = 5
        
        # Should not raise exception for own resource
        ensure_access(user, resource_user_id=5, resource_name="profile")
    
    def test_ensure_access_denied(self):
        """Should raise HTTPException when access denied"""
        user = Mock(spec=User)
        user.is_admin = False
        user.id = 5
        
        # Should raise exception for other user's resource
        with pytest.raises(HTTPException) as exc_info:
            ensure_access(user, resource_user_id=999, resource_name="profile")
        
        assert exc_info.value.status_code == 403
        assert "Cannot access profile" in str(exc_info.value.message)
    
    def test_ensure_access_default_resource_name(self):
        """Test default resource name in error message"""
        user = Mock(spec=User)
        user.is_admin = False
        user.id = 5
        
        with pytest.raises(HTTPException) as exc_info:
            ensure_access(user, resource_user_id=999)  # No resource_name provided
        
        assert exc_info.value.status_code == 403
        assert "Cannot access resource" in str(exc_info.value.message)


@pytest.mark.asyncio
class TestAdminRequiredDependency:
    """Test admin_required FastAPI dependency"""
    
    async def test_admin_required_with_admin_user(self):
        """Admin user should pass admin_required check"""
        admin_user = Mock(spec=User)
        admin_user.is_admin = True
        admin_user.role = UserRole.ADMIN
        
        # Should return the admin user
        result = await admin_required(admin_user)
        assert result == admin_user
    
    async def test_admin_required_with_regular_user(self):
        """Regular user should fail admin_required check"""
        regular_user = Mock(spec=User)
        regular_user.is_admin = False
        regular_user.role = UserRole.USER
        
        # Should raise HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await admin_required(regular_user)
        
        assert exc_info.value.status_code == 403
        assert "Admin access required" in str(exc_info.value.message)
    
    async def test_require_admin_alias(self):
        """Test that require_admin alias works the same"""
        admin_user = Mock(spec=User)
        admin_user.is_admin = True
        
        # Both should work identically
        result1 = await admin_required(admin_user)
        result2 = await require_admin(admin_user)
        
        assert result1 == result2 == admin_user
    
    async def test_admin_required_with_inactive_admin(self):
        """Test edge case: user has admin role but is_admin property is False"""
        user = Mock(spec=User)
        user.is_admin = False  # This should be the deciding factor
        user.role = UserRole.ADMIN  # Role is admin but is_admin property is False
        
        with pytest.raises(HTTPException) as exc_info:
            await admin_required(user)
        
        assert exc_info.value.status_code == 403
        assert "Admin access required" in str(exc_info.value.message)


class TestRoleBasedScenarios:
    """Test real-world RBAC scenarios"""
    
    def test_user_accessing_own_profile(self):
        """User should be able to access their own profile"""
        user = Mock(spec=User)
        user.is_admin = False
        user.id = 123
        user.role = UserRole.USER
        
        # User accessing their own profile (user_id = 123)
        assert check_access(user, resource_user_id=123) == True
        
        # Should not raise exception
        ensure_access(user, resource_user_id=123, resource_name="profile")
    
    def test_user_accessing_other_profile(self):
        """User should NOT be able to access other user's profile"""
        user = Mock(spec=User)
        user.is_admin = False
        user.id = 123
        user.role = UserRole.USER
        
        # User trying to access another user's profile (user_id = 456)
        assert check_access(user, resource_user_id=456) == False
        
        # Should raise exception
        with pytest.raises(HTTPException) as exc_info:
            ensure_access(user, resource_user_id=456, resource_name="profile")
        
        assert exc_info.value.status_code == 403
    
    def test_admin_accessing_any_profile(self):
        """Admin should be able to access any user's profile"""
        admin = Mock(spec=User)
        admin.is_admin = True
        admin.id = 1
        admin.role = UserRole.ADMIN
        
        # Admin accessing different users' profiles
        assert check_access(admin, resource_user_id=123) == True
        assert check_access(admin, resource_user_id=456) == True
        assert check_access(admin, resource_user_id=999) == True
        
        # Should not raise exceptions
        ensure_access(admin, resource_user_id=123, resource_name="profile")
        ensure_access(admin, resource_user_id=456, resource_name="resume")
        ensure_access(admin, resource_user_id=999, resource_name="data")
    
    def test_admin_accessing_own_profile(self):
        """Admin should be able to access their own profile (obviously)"""
        admin = Mock(spec=User)
        admin.is_admin = True
        admin.id = 1
        admin.role = UserRole.ADMIN
        
        # Admin accessing their own profile
        assert check_access(admin, resource_user_id=1) == True
        ensure_access(admin, resource_user_id=1, resource_name="profile")


class TestEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_check_access_with_none_user_id(self):
        """Test behavior when resource_user_id is None or 0"""
        user = Mock(spec=User)
        user.is_admin = False
        user.id = 123
        
        # These should return False for regular users
        assert check_access(user, resource_user_id=None) == False
        assert check_access(user, resource_user_id=0) == False
    
    def test_admin_check_access_with_none_user_id(self):
        """Admin should have access even with None/0 user_id"""
        admin = Mock(spec=User)
        admin.is_admin = True
        admin.id = 1
        
        # Admin should have access regardless
        assert check_access(admin, resource_user_id=None) == True
        assert check_access(admin, resource_user_id=0) == True
    
    def test_ensure_access_with_custom_resource_names(self):
        """Test ensure_access with different resource names"""
        user = Mock(spec=User)
        user.is_admin = False
        user.id = 123
        
        # Test different resource names in error messages
        test_cases = ["resume", "profile", "document", "settings"]
        
        for resource_name in test_cases:
            with pytest.raises(HTTPException) as exc_info:
                ensure_access(user, resource_user_id=999, resource_name=resource_name)
            
            assert f"Cannot access {resource_name}" in str(exc_info.value.message)
