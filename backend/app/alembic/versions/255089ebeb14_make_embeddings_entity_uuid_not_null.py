"""make embeddings entity_uuid NOT NULL

Revision ID: 255089ebeb14
Revises: 91f90c2b89ae
Create Date: 2026-06-05 17:51:31.290506

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '255089ebeb14'
down_revision: Union[str, Sequence[str], None] = '91f90c2b89ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('embeddings', 'entity_uuid',
               existing_type=sa.UUID(),
               nullable=False)


def downgrade() -> None:
    op.alter_column('embeddings', 'entity_uuid',
               existing_type=sa.UUID(),
               nullable=True)
