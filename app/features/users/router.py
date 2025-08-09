from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.dependencies import get_db
from features.users.service import UserService
from features.users.schemas import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    service = UserService(db)
    try:
        return service.create_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_uuid}", response_model=UserResponse)
def get_user(user_uuid: str, db: Session = Depends(get_db)):
    """Get user by UUID"""
    service = UserService(db)
    user = service.get_user_by_uuid(user_uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=List[UserResponse])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all users with pagination"""
    service = UserService(db)
    return service.list_users(skip, limit)

@router.put("/{user_uuid}", response_model=UserResponse)
def update_user(user_uuid: str, user_data: UserUpdate, db: Session = Depends(get_db)):
    """Update user information"""
    service = UserService(db)
    # First get user by UUID to get the ID
    user = service.get_user_by_uuid(user_uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    updated_user = service.update_user_by_uuid(user_uuid, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_uuid: str, db: Session = Depends(get_db)):
    """Delete a user"""
    service = UserService(db)
    if not service.delete_user_by_uuid(user_uuid):
        raise HTTPException(status_code=404, detail="User not found")
