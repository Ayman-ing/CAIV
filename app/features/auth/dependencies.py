from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional

from core.dependencies import get_db
from features.users.models import User
from .service import AuthService

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