from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from features.users.models import User
from core.dependencies import  get_db
from features.auth.dependencies import get_current_user
from features.users.service import UserService
from features.users.schemas import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/api/v1", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    service = UserService(db)
    try:
        return service.create_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me", response_model=UserResponse)
def get_user_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get current user information"""
    service = UserService(db)
    user = service.get_user_by_uuid(current_user.uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=List[UserResponse])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all users with pagination"""
    service = UserService(db)
    return service.list_users(skip, limit)

@router.put("/me", response_model=UserResponse)
def update_user_me(user_data: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Update current user information"""
    service = UserService(db)
    # First get user by UUID to get the ID
    user = service.get_user_by_uuid(current_user.uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    updated_user = service.update_user_by_uuid(user.uuid, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_uuid: str, db: Session = Depends(get_db)):
    """Delete a user"""
    service = UserService(db)
    if not service.delete_user_by_uuid(user_uuid):
        raise HTTPException(status_code=404, detail="User not found")
