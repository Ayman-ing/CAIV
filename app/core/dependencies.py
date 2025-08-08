from sqlalchemy.orm import Session
from typing import Generator
from app.db.session import SessionLocal

def get_db() -> Generator[Session, None, None]:
    """
    Dependency function that yields database sessions
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
