from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from features.users.models import User
from .schemas import UserRegister, Token, PasswordChange, PasswordReset, PasswordResetConfirm
from .service import AuthService
from .dependencies import get_current_user, get_auth_service

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Register a new user"""
    user, access_token = auth_service.register_user(user_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 1800,  # 30 minutes in seconds
        "user_id": str(user.uuid)
    }

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Login user and return JWT token"""
    user, access_token = auth_service.authenticate_user(form_data.username, form_data.password)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 1800,  # 30 minutes in seconds
        "user_id": str(user.uuid)
    }

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """Logout user (client should discard the token)"""
    return {"message": "Successfully logged out"}

@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Change user password"""
    auth_service.change_user_password(current_user, password_data)
    return {"message": "Password changed successfully"}

@router.post("/request-password-reset")
async def request_password_reset(
    password_reset: PasswordReset,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Request password reset"""
    reset_token = auth_service.request_password_reset(password_reset)
    
    if reset_token:
        # In production, send this token via email
        return {
            "message": "Password reset token generated",
            "reset_token": reset_token  # Remove this in production!
        }
    else:
        return {"message": "If the email exists, a password reset link has been sent"}

@router.post("/reset-password")
async def reset_password(
    reset_data: PasswordResetConfirm,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Reset password using reset token"""
    auth_service.reset_user_password(reset_data)
    return {"message": "Password reset successfully"}

@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user information"""
    return {
        "id": current_user.id,
        "uuid": current_user.uuid,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "location": current_user.location,
        "phone_number": current_user.phone_number,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at,
        "updated_at": current_user.updated_at
    }