"""make vector_data native pgvector vector(384) type

Revision ID: def789abc012
Revises: abc123def456
Create Date: 2026-05-21 11:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


revision: str = 'def789abc012'
down_revision: Union[str, Sequence[str], None] = 'abc123def456'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Enable pgvector extension if not already enabled
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')

    # Drop old text-based index if it exists
    op.execute('DROP INDEX IF EXISTS idx_embeddings_vector')

    # Change vector_data from Text to native vector(384)
    # USING clause converts existing text-formatted vectors to native type
    op.alter_column(
        'embeddings', 'vector_data',
        type_=Vector(384),
        postgresql_using='vector_data::vector(384)',
        existing_type=sa.Text(),
        existing_nullable=True,
    )

    # Create ivfflat index for cosine similarity search
    op.execute(
        'CREATE INDEX IF NOT EXISTS idx_embeddings_vector ON embeddings '
        'USING ivfflat (vector_data vector_cosine_ops) '
        'WITH (lists = 100)'
    )


def downgrade() -> None:
    op.execute('DROP INDEX IF EXISTS idx_embeddings_vector')

    op.alter_column(
        'embeddings', 'vector_data',
        type_=sa.Text(),
        postgresql_using='vector_data::text',
        existing_type=Vector(384),
        existing_nullable=True,
    )
