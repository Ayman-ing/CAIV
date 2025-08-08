from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Construct the SQLAlchemy connection string
DATABASE_URL = os.getenv("database_url")

# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "connect_timeout": 30,
        "application_name": "caiv_app"
    }
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
