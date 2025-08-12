"""
Simple and efficient RBAC for AI Resume Builder
"""
from fastapi import Depends, HTTPException, status
from features.users.models import User
from features.auth.dependencies import get_current_user


async def admin_required(current_user: User = Depends(get_current_user)) -> User:
    """Dependency: Require admin role"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


def check_access(current_user: User, resource_user_id: int) -> bool:
    """Check if user can access resource (admin or owner)"""
    return current_user.is_admin or current_user.id == resource_user_id


def ensure_access(current_user: User, resource_user_id: int, resource_name: str = "resource"):
    """Raise error if user cannot access resource"""
    if not check_access(current_user, resource_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Cannot access {resource_name}"
        )


# Alias for clarity
require_admin = admin_required