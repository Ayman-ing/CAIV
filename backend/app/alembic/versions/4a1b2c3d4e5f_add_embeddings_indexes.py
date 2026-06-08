"""Add indexes on embeddings(entity_uuid, indexed_at) for faster per-entity status queries

Revision ID: 4a1b2c3d4e5f
Revises: 3dcf1b4560cf
Create Date: 2026-06-06 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '4a1b2c3d4e5f'
down_revision: Union[str, Sequence[str], None] = '3dcf1b4560cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('CREATE INDEX IF NOT EXISTS idx_embeddings_entity_uuid ON embeddings (entity_uuid)')
    op.execute('CREATE INDEX IF NOT EXISTS idx_embeddings_indexed_at ON embeddings (indexed_at)')


def downgrade() -> None:
    op.drop_index('idx_embeddings_indexed_at', table_name='embeddings')
    op.drop_index('idx_embeddings_entity_uuid', table_name='embeddings')
