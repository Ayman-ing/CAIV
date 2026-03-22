"""Fix professional_summaries schema - replace summary_text with title and content

Revision ID: fix_professional_summaries
Revises: 972a28112e99
Create Date: 2025-03-19 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fix_professional_summaries'
down_revision: Union[str, Sequence[str], None] = '972a28112e99'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - add title and content columns to professional_summaries."""
    with op.batch_alter_table('professional_summaries', schema=None) as batch_op:
        # Add title column
        batch_op.add_column(sa.Column('title', sa.String(), nullable=True))
        
        # Add content column
        batch_op.add_column(sa.Column('content', sa.String(), nullable=True))
        
        # Drop summary_text column if it exists
        try:
            batch_op.drop_column('summary_text')
        except Exception:
            pass  # Column might not exist


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('professional_summaries', schema=None) as batch_op:
        batch_op.add_column(sa.Column('summary_text', sa.String(), nullable=True))
        
        try:
            batch_op.drop_column('title')
        except Exception:
            pass
        
        try:
            batch_op.drop_column('content')
        except Exception:
            pass
