from datetime import datetime, timedelta
from typing import Optional, Tuple
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
import os
from sqlalchemy.orm import Session

from features.users.models import User
from .repository import AuthRepository
from .schemas import UserRegister, PasswordChange, PasswordReset, PasswordResetConfirm

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = os.getenv("JWT_SECRET", os.getenv("JWT_SECRET"))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.auth_repo = AuthRepository(db)
    
    # Static methods for password and token operations
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "iat": datetime.utcnow()})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> dict:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    # Business logic methods
    def register_user(self, user_data: UserRegister) -> Tuple[User, str]:
        """Register a new user and return user + access token"""
        # Check if user already exists
        if self.auth_repo.email_exists(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        hashed_password = self.get_password_hash(user_data.password)
        user = self.auth_repo.create_user(
            email=user_data.email, 
            password_hash=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        
        # Create access token
        access_token = self.create_access_token(data={"sub": str(user.uuid)})
        
        return user, access_token
    
    def authenticate_user(self, email: str, password: str) -> Tuple[User, str]:
        """Authenticate user and return user + access token"""
        # Find user by email
        user = self.auth_repo.get_user_by_email(email)
        
        # Verify user exists and password is correct
        if not user or not self.verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token = self.create_access_token(data={"sub": str(user.uuid)})

        return user, access_token
    
    def change_user_password(self, user: User, password_data: PasswordChange) -> None:
        """Change user password"""
        # Verify current password
        if not self.verify_password(password_data.current_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Update password
        new_password_hash = self.get_password_hash(password_data.new_password)
        self.auth_repo.update_user_password(user, new_password_hash)
    
    def request_password_reset(self, password_reset: PasswordReset) -> Optional[str]:
        """Request password reset and return reset token if user exists"""
        user = self.auth_repo.get_user_by_email(password_reset.email)
        if not user:
            # Don't reveal if email exists for security
            return None
        
        # Generate password reset token
        reset_token = self.create_password_reset_token(user.email)
        return reset_token
    
    def reset_user_password(self, reset_data: PasswordResetConfirm) -> None:
        """Reset user password using reset token"""
        # Verify reset token and get email
        email = self.verify_password_reset_token(reset_data.token)
        
        # Find user
        user = self.auth_repo.get_user_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Update password
        new_password_hash = self.get_password_hash(reset_data.new_password)
        self.auth_repo.update_user_password(user, new_password_hash)
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.auth_repo.get_user_by_id(user_id)
    
    def get_user_by_uuid(self, user_uuid: str) -> Optional[User]:
        """Get user by UUID"""
        return self.auth_repo.get_user_by_uuid(user_uuid)
    
    @staticmethod
    def create_password_reset_token(email: str) -> str:
        """Create a password reset token (expires in 1 hour)"""
        expire = datetime.utcnow() + timedelta(hours=1)
        to_encode = {"sub": email, "exp": expire, "type": "password_reset"}
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    @staticmethod
    def verify_password_reset_token(token: str) -> str:
        """Verify password reset token and return email"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
            token_type = payload.get("type")
            
            if email is None or token_type != "password_reset":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid password reset token"
                )
            return email
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password reset token has expired"
            )
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid password reset token"
            )