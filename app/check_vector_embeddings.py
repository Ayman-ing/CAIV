#!/usr/bin/env python3

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_vector_embeddings_structure():
    """Check the structure of the vector_embeddings table"""
    
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
            # Get columns info for vector_embeddings
            result = connection.execute(text("""
                SELECT 
                    column_name, 
                    data_type, 
                    is_nullable,
                    column_default
                FROM information_schema.columns 
                WHERE table_name = 'vector_embeddings'
                ORDER BY ordinal_position;
            """))
            
            columns = result.fetchall()
            
            print(f"🔍 Vector Embeddings Table Structure:")
            print(f"{'Column Name':<25} {'Data Type':<20} {'Nullable':<10} {'Default'}")
            print("-" * 80)
            
            for col in columns:
                column_name, data_type, is_nullable, column_default = col
                default_str = str(column_default)[:20] if column_default else "None"
                print(f"{column_name:<25} {data_type:<20} {is_nullable:<10} {default_str}")
            
            # Check foreign key constraints
            fk_result = connection.execute(text("""
                SELECT
                    kcu.column_name,
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name
                FROM information_schema.key_column_usage AS kcu
                JOIN information_schema.constraint_column_usage AS ccu
                    ON kcu.constraint_name = ccu.constraint_name
                WHERE kcu.table_name = 'vector_embeddings'
                AND kcu.constraint_name IN (
                    SELECT constraint_name
                    FROM information_schema.table_constraints
                    WHERE constraint_type = 'FOREIGN KEY'
                    AND table_name = 'vector_embeddings'
                )
                ORDER BY kcu.column_name;
            """))
            
            foreign_keys = fk_result.fetchall()
            
            print(f"\n🔗 Foreign Key Relationships:")
            print(f"{'Column':<25} {'References Table':<20} {'References Column'}")
            print("-" * 70)
            
            for fk in foreign_keys:
                column_name, foreign_table, foreign_column = fk
                print(f"{column_name:<25} {foreign_table:<20} {foreign_column}")
                
            print(f"\n✅ Vector embeddings table now has {len(foreign_keys)} proper foreign key relationships!")
                
    except Exception as e:
        print(f"❌ Error checking vector embeddings structure: {e}")

if __name__ == "__main__":
    check_vector_embeddings_structure()
