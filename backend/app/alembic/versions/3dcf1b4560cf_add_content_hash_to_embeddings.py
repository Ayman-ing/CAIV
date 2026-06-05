"""add content_hash to embeddings

Revision ID: 3dcf1b4560cf
Revises: 255089ebeb14
Create Date: 2026-06-05 18:42:36.184823

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '3dcf1b4560cf'
down_revision: Union[str, Sequence[str], None] = '255089ebeb14'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('embeddings', sa.Column('content_hash', sa.String(length=64), nullable=True))


def downgrade() -> None:
    op.drop_column('embeddings', 'content_hash')
