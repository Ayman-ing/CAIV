from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the parent directory to the path so we can import our models
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import the Base class first to avoid circular imports
from shared.models.base import Base

# Import all models to ensure they're registered with SQLAlchemy
try:
    # Import Base first
    from shared.models.base import Base
    
    # Import models directly from their files, not through feature packages
    import sys
    import importlib.util
    
    model_files = [
        ("entity_models", "shared/models/entity.py"),  # Import entity models first
        ("users_models", "features/users/models.py"),
        ("profiles_models", "features/profiles/models.py"),
        ("resumes_models", "features/resumes/models.py"),
        ("job_descriptions_models", "features/job_descriptions/models.py"),
        ("job_keywords_models", "features/job_keywords/models.py"),
        ("job_requirements_models", "features/job_requirements/models.py"),
        ("outbox_events_models", "features/outbox_events/models.py"),
        ("vector_embeddings_models", "features/vector_embeddings/models.py"),
        ("custom_sections_models", "features/profiles/custom_sections/models.py"),
        ("profile_links_models", "features/profiles/profile_links/models.py"),
        ("professional_summaries_models", "features/profiles/professional_summaries/models.py"),
        ("work_experiences_models", "features/profiles/work_experiences/models.py"),
        ("education_models", "features/profiles/education/models.py"),
        ("skills_models", "features/profiles/skills/models.py"),
        ("projects_models", "features/profiles/projects/models.py"),
        ("certificates_models", "features/profiles/certificates/models.py"),
        ("languages_models", "features/profiles/languages/models.py"),
    ]
    
    for module_name, file_path in model_files:
        try:
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                print(f"✅ Imported {file_path}")
        except Exception as e:
            print(f"⚠️  Warning: Could not import {file_path}: {e}")
    
    print(f"✅ Successfully imported models")
    print(f"📊 Found {len(Base.metadata.tables)} tables to create:")
    for table_name in sorted(Base.metadata.tables.keys()):
        print(f"  - {table_name}")
        
except Exception as e:
    print(f"❌ Error importing models: {e}")
    import traceback
    traceback.print_exc()

config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def get_url():
    """Get database URL from environment variable or config"""
    url = os.getenv("DATABASE_URL") or os.getenv("database_url")
    if not url:
        url = config.get_main_option("sqlalchemy.url")
    
    if not url:
        raise ValueError("No database URL found. Please set DATABASE_URL environment variable.")
    
    # Fix common PostgreSQL URL issues
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    
    # Ensure the URL has the correct driver
    if url.startswith("postgresql://") and "+psycopg2" not in url:
        # Check if it already has a driver specified
        if "://" in url and "@" in url:
            protocol, rest = url.split("://", 1)
            if "+" not in protocol:
                url = f"postgresql+psycopg2://{rest}"
    
    print(f"Using database URL: {url.split('@')[0]}@***")  # Hide password
    return url

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    # Override the sqlalchemy.url with environment variable if available
    configuration = config.get_section(config.config_ini_section)
    database_url = get_url()
    if database_url:
        configuration["sqlalchemy.url"] = database_url

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()