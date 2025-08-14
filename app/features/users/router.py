from fastapi import APIRouter, Depends, status
from core.exceptions import HTTPException
from sqlalchemy.orm import Session
from typing import List

from features.auth.service import AuthService
from features.auth.schemas import TokenData, UserRegister
from features.users.models import User, UserRole
from db.session import  get_db
from features.auth.dependencies import get_current_user_from_token, require_admin_from_token
from features.users.service import UserService
from features.users.schemas import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/api/v1", tags=["users"])



@router.get("/me", response_model=UserResponse)
def get_user_me(current_user: TokenData = Depends(get_current_user_from_token), db: Session = Depends(get_db)):
    """Get current user information"""
    service = UserService(db)
    user = service.get_user_by_uuid(current_user.user_id)
    if not user:
        raise HTTPException(status_code=404, message="User not found")
    return user



@router.put("/me", response_model=UserResponse)
def update_user_me(user_data: UserUpdate, current_user: TokenData = Depends(get_current_user_from_token), db: Session = Depends(get_db)):
    """Update current user information"""
    service = UserService(db)
    # First get user by UUID to get the ID
    user = service.get_user_by_uuid(current_user.user_id)
    if not user:
        raise HTTPException(status_code=404, message="User not found")

    updated_user = service.update_user_by_uuid(user.uuid, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, message="User not found")
    return updated_user

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_user( db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user_from_token)):
    """Delete a user"""
    service = UserService(db)
    if not service.delete_user_by_uuid(current_user.user_id):
        raise HTTPException(status_code=404, message="User not found")


# Admin-only routes
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db), admin_user: TokenData = Depends(require_admin_from_token)):
    """Create a new user"""
    from features.auth.service import AuthService
    from features.auth.schemas import UserRegister
    
    auth_service = AuthService(db)
    try:
        # Convert UserCreate to UserRegister (excluding role which is handled separately)
        user_register = UserRegister(
            email=user_data.email,
            password=user_data.password,
            confirm_password=user_data.confirm_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        # Pass the role from UserCreate to register_user
        user, access_token = auth_service.register_user(user_register, role=user_data.role)
        
        # Convert User to UserResponse
        return UserResponse.model_validate(user)
    except ValueError as e:
        raise HTTPException(status_code=400, message=str(e))
    
@router.get("/", response_model=List[UserResponse])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), admin_user: TokenData = Depends(require_admin_from_token)):
    """List all users with pagination - Admin only"""
    service = UserService(db)
    return service.list_users(skip, limit)
@router.get("/{user_uuid}", response_model=UserResponse)
def get_user_by_uuid_admin(user_uuid: str, db: Session = Depends(get_db), admin_user: TokenData = Depends(require_admin_from_token)):
    """Get user by UUID - Admin only"""
    service = UserService(db)
    user = service.get_user_by_uuid(user_uuid)
    if not user:
        raise HTTPException(status_code=404, message="User not found")
    return user


@router.put("/{user_uuid}", response_model=UserResponse)
def update_user_by_uuid_admin(user_uuid: str, user_data: UserUpdate, db: Session = Depends(get_db), admin_user: TokenData = Depends(require_admin_from_token)):
    """Update user by UUID - Admin only"""
    service = UserService(db)
    updated_user = service.update_user_by_uuid(user_uuid, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, message="User not found")
    return updated_user


@router.delete("/{user_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_by_uuid_admin(user_uuid: str, db: Session = Depends(get_db), admin_user: TokenData = Depends(require_admin_from_token)):
    """Delete user by UUID - Admin only"""
    service = UserService(db)
    if not service.delete_user_by_uuid(user_uuid):
        raise HTTPException(status_code=404, message="User not found")


@router.post("/{user_uuid}/promote", response_model=UserResponse)
def promote_user_to_admin(user_uuid: str, db: Session = Depends(get_db), admin_user: TokenData = Depends(require_admin_from_token)):
    """Promote user to admin role - Admin only"""
    service = UserService(db)
    user = service.get_user_by_uuid(user_uuid)
    if not user:
        raise HTTPException(status_code=404, message="User not found")

    if user.role == UserRole.ADMIN:
        raise HTTPException(status_code=400, message="User is already an admin")
    
    # Update user role to admin
    user_data = UserUpdate(role=UserRole.ADMIN)
    updated_user = service.update_user_by_uuid(user_uuid, user_data)
    return updated_user
