from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()
engine = create_engine(os.getenv('DATABASE_URL') or os.getenv('database_url'))

with engine.connect() as conn:
    result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name"))
    tables = [row[0] for row in result.fetchall()]
    print(f'🎉 Successfully created {len(tables)} tables:')
    for table in tables:
        print(f'✅ {table}')
