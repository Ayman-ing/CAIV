from http.client import HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Generator
import jwt
from fastapi.security import OAuth2PasswordBearer
import os
from db.session import SessionLocal
from features.users.models import User
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Define JWT_SECRET and JWT_ALGORITHM
JWT_SECRET = os.getenv("JWT_SECRET", "your_default_secret")
JWT_ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db() -> Generator[Session, None, None]:
    """
    Dependency function that yields database sessions
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    """
    Dependency to get the current user from the token
  """
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    user = db.query(User).filter(User.id == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user  
