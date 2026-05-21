"""fix embeddings table schema to match model

Revision ID: abc123def456
Revises: a1b2c3d4e5f6
Create Date: 2026-05-21 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = 'abc123def456'
down_revision: Union[str, Sequence[str], None] = ['a1b2c3d4e5f6', 'create_uploaded_resumes']
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Enable pgvector extension if not already enabled
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')

    # Drop the old vector_embeddings table (created by the original migration
    # but never used by the current model which expects 'embeddings')
    op.execute('DROP TABLE IF EXISTS vector_embeddings CASCADE')

    # Drop embeddings table if it exists (may have been partially created
    # with wrong columns by the previous migration)
    op.execute('DROP TABLE IF EXISTS embeddings CASCADE')

    # Create embeddings table matching the SQLAlchemy model exactly
    op.create_table('embeddings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('entity_uuid', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('entities.uuid'), nullable=True),
        sa.Column('vector_data', sa.Text(), nullable=True),
        sa.Column('embedding_type', sa.String(50), nullable=False),
        sa.Column('chunk_index', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('text_preview', sa.Text(), nullable=True),
        sa.Column('token_count', sa.Integer(), nullable=True),
        sa.Column('model_name', sa.String(100), nullable=True),
        sa.Column('model_version', sa.String(50), nullable=True),
        sa.Column('metadata_json', sa.Text(), nullable=True),
        sa.Column('status', sa.String(50), nullable=True, server_default='pending'),
        sa.Column('indexed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('uuid'),
    )

    op.create_index('idx_embeddings_entity_uuid', 'embeddings', ['entity_uuid'])
    op.create_index('idx_embeddings_type_chunk', 'embeddings',
                    ['entity_uuid', 'embedding_type', 'chunk_index'])
    # Note: vector_data is stored as Text (pgvector-formatted string).
    # To add ivfflat index for similarity search, vector_data must be native vector(384).
    # This requires changing the SQLAlchemy model to use Vector type and
    # adding the pgvector extension dependency.


def downgrade() -> None:
    op.drop_index('idx_embeddings_type_chunk', table_name='embeddings')
    op.drop_index('idx_embeddings_entity_uuid', table_name='embeddings')
    op.drop_table('embeddings')
