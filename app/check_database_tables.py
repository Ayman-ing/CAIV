#!/usr/bin/env python3

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_tables():
    """Check what tables exist in the database"""
    
    # Get database URL
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        return
    
    # Fix PostgreSQL URL if needed
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    if "+psycopg2" not in database_url:
        database_url = database_url.replace("postgresql://", "postgresql+psycopg2://")
    
    try:
        # Create engine
        engine = create_engine(database_url)
        
        with engine.connect() as connection:
            # Get all tables
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name;
            """))
            
            tables = [row[0] for row in result.fetchall()]
            
            print(f"✅ Found {len(tables)} tables in the database:")
            for table in tables:
                print(f"  📋 {table}")
            
            # Check for our expected tables
            expected_tables = [
                'users', 'profiles', 'generated_resumes', 'resume_components',
                'job_descriptions', 'job_keywords', 'job_requirements',
                'education', 'work_experiences', 'projects', 'skills',
                'certificates', 'languages', 'professional_summaries',
                'profile_links', 'custom_sections', 'outbox_events',
                'vector_embeddings', 'alembic_version'
            ]
            
            missing_tables = [table for table in expected_tables if table not in tables]
            if missing_tables:
                print(f"\n⚠️  Missing expected tables: {missing_tables}")
            else:
                print(f"\n✅ All expected tables are present!")
                
    except Exception as e:
        print(f"❌ Error checking tables: {e}")

if __name__ == "__main__":
    check_tables()
