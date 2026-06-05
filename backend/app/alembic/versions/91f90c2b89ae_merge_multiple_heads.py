"""merge multiple heads

Revision ID: 91f90c2b89ae
Revises: create_resume_drafts, def789abc012
Create Date: 2026-06-04 23:04:50.890646

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '91f90c2b89ae'
down_revision: Union[str, Sequence[str], None] = ('create_resume_drafts', 'def789abc012')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
