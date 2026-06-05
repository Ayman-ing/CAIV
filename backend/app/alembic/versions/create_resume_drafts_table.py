"""Create resume_drafts table

Revision ID: create_resume_drafts
Revises: 290bf9bbc390
Create Date: 2026-06-04

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB


revision: str = 'create_resume_drafts'
down_revision: Union[str, None] = '290bf9bbc390'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'resume_drafts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('uuid', UUID(as_uuid=True), unique=True, nullable=False),
        sa.Column('profile_id', sa.Integer(), sa.ForeignKey('profiles.id'), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('template_name', sa.String(), nullable=True),
        sa.Column('draft_data', JSONB(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('resume_drafts')
