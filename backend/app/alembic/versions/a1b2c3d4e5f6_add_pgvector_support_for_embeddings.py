"""add pgvector support for embeddings

Revision ID: a1b2c3d4e5f6
Revises: f52b4d37cafa
Create Date: 2026-05-20 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = 'f52b4d37cafa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema to use pgvector for embeddings."""
    # Enable pgvector extension
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')
    
    # Drop the old qdrant_point_id column and add vector_data column
    op.drop_column('embeddings', 'qdrant_point_id')
    
    # Add vector column with 384 dimensions (for all-MiniLM-L6-v2)
    op.execute('ALTER TABLE embeddings ADD COLUMN IF NOT EXISTS vector_data vector(384)')
    
    # Add indexing status columns
    op.add_column('embeddings', sa.Column('indexed_at', sa.DateTime(), nullable=True))
    op.add_column('embeddings', sa.Column(
        'status',
        sa.String(50),
        nullable=True,
        server_default='pending'
    ))
    
    # Create vector index using ivfflat for similarity search
    # Note: This needs to be done after data migration if there's existing data
    op.execute(
        'CREATE INDEX IF NOT EXISTS idx_embeddings_vector ON embeddings USING ivfflat (vector_data vector_cosine_ops)'
    )


def downgrade() -> None:
    """Downgrade schema to remove pgvector support."""
    # Drop vector index
    op.execute('DROP INDEX IF EXISTS idx_embeddings_vector')
    
    # Remove new columns
    op.drop_column('embeddings', 'status')
    op.drop_column('embeddings', 'indexed_at')
    
    # Drop vector column and restore qdrant_point_id
    op.execute('ALTER TABLE embeddings DROP COLUMN IF EXISTS vector_data')
    op.add_column('embeddings', sa.Column(
        'qdrant_point_id',
        postgresql.UUID(),
        unique=True,
        nullable=False
    ))
    
    # Disable pgvector extension
    op.execute('DROP EXTENSION IF EXISTS vector')
