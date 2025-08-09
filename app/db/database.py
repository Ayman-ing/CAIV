from sqlalchemy import create_engine
# from sqlalchemy.pool import NullPool
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Import all models to ensure they're registered with SQLAlchemy
from shared.models.registry import Base

# Construct the SQLAlchemy connection string
DATABASE_URL = os.getenv("database_url")

# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "connect_timeout": 30,
        "application_name": "caiv_app"
    },
    pool_pre_ping=True
)
# If using Transaction Pooler or Session Pooler, we want to ensure we disable SQLAlchemy client side pooling -
# https://docs.sqlalchemy.org/en/20/core/pooling.html#switching-pool-implementations
# engine = create_engine(DATABASE_URL, poolclass=NullPool)

# Test the connection
def test_db_connection(): 
    try:
        with engine.connect() as connection:
            print("Connection successful!")
            print(f"Connected to: {DATABASE_URL}")
    except Exception as e:
        print(f"Failed to connect: {e}")

def create_tables():
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)