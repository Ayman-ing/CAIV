"""add is_default to professional_summaries

Revision ID: add_is_default_summaries
Revises: fix_professional_summaries
Create Date: 2025-01-09 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_is_default_summaries'
down_revision = 'fix_professional_summaries'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add is_default column with default value of False
    op.add_column('professional_summaries', sa.Column('is_default', sa.Boolean(), nullable=False, server_default=sa.false()))
    # Remove server default after applying
    op.alter_column('professional_summaries', 'is_default', server_default=None)


def downgrade() -> None:
    # Remove the is_default column
    op.drop_column('professional_summaries', 'is_default')
