from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from db.session import get_db
from features.users.models import User, UserRole
from .service import AuthService
from .schemas import TokenData

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """Dependency to get AuthService instance"""
    return AuthService(db)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service)
) -> User:
    """
    Dependency to get the current authenticated user from JWT token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Verify and decode JWT token
        payload = AuthService.verify_token(token)
        user_uuid: str = payload.get("sub")
        if user_uuid is None:
            raise credentials_exception
    except HTTPException:
        raise credentials_exception
    
    # Get user from database via service
    user = auth_service.get_user_by_uuid(user_uuid)
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to get current active user
    """
    return current_user

async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme)
) -> TokenData:
    """
    Dependency to get current user data directly from JWT token (no DB call)
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Verify and decode JWT token
        payload = AuthService.verify_token(token)
        user_uuid: str = payload.get("sub")
        role: str = payload.get("role")
        
        if user_uuid is None:
            raise credentials_exception
            
        return TokenData(
            user_id=UUID(user_uuid),
            role=role
        )
    except HTTPException:
        raise credentials_exception
    except ValueError:  # Invalid UUID
        raise credentials_exception

def get_optional_current_user(
    auth_service: AuthService = Depends(get_auth_service),
    token: Optional[str] = Depends(oauth2_scheme)
) -> Optional[User]:
    """
    Optional authentication - returns user if authenticated, None if not
    """
    if not token:
        return None
    
    try:
        payload = AuthService.verify_token(token)
        user_uuid: str = payload.get("sub")
        if user_uuid is None:
            return None
        
        user = auth_service.get_user_by_uuid(user_uuid)
        return user
    except:
        return None

async def require_admin_from_token(
    token_data: TokenData = Depends(get_current_user_from_token)
) -> TokenData:
    """
    Dependency to require admin role using token data (no DB call)
    """
    if token_data.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return token_data

def check_access_from_token(
    token_data: TokenData,
    resource_user_id: str
) -> bool:
    """
    Check if user can access resource using token data (admin or owner)
    """
    return (token_data.role == UserRole.ADMIN.value or 
            str(token_data.user_id) == resource_user_id)

def ensure_access_from_token(
    token_data: TokenData,
    resource_user_id: str,
    resource_name: str = "resource"
):
    """
    Raise error if user cannot access resource using token data
    """
    if not check_access_from_token(token_data, resource_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Cannot access {resource_name}"
        )