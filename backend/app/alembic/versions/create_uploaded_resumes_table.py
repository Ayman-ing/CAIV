"""Create uploaded_resumes table for tracking resume imports

Revision ID: create_uploaded_resumes
Revises: fix_professional_summaries
Create Date: 2026-05-20 23:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'create_uploaded_resumes'
down_revision: Union[str, Sequence[str], None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create uploaded_resumes table."""
    op.create_table(
        'uploaded_resumes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('profile_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('original_filename', sa.String(length=255), nullable=False),
        sa.Column('extracted_data', sa.JSON(), nullable=False),
        sa.Column('import_status', sa.String(length=50), nullable=False, server_default='pending'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('uuid')
    )
    op.create_index(op.f('ix_uploaded_resumes_profile_id'), 'uploaded_resumes', ['profile_id'], unique=False)
    op.create_index(op.f('ix_uploaded_resumes_user_id'), 'uploaded_resumes', ['user_id'], unique=False)
    op.create_index(op.f('ix_uploaded_resumes_uuid'), 'uploaded_resumes', ['uuid'], unique=False)


def downgrade() -> None:
    """Drop uploaded_resumes table."""
    op.drop_index(op.f('ix_uploaded_resumes_uuid'), table_name='uploaded_resumes')
    op.drop_index(op.f('ix_uploaded_resumes_user_id'), table_name='uploaded_resumes')
    op.drop_index(op.f('ix_uploaded_resumes_profile_id'), table_name='uploaded_resumes')
    op.drop_table('uploaded_resumes')
