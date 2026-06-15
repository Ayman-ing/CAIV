"""Add missing title, company, content columns to job_descriptions

Revision ID: add_jd_missing_columns
Revises: 4a1b2c3d4e5f
Create Date: 2026-06-15

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = 'add_jd_missing_columns'
down_revision: Union[str, None] = '4a1b2c3d4e5f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('job_descriptions', sa.Column('title', sa.String(), nullable=True))
    op.add_column('job_descriptions', sa.Column('company', sa.String(), nullable=True))
    op.add_column('job_descriptions', sa.Column('content', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('job_descriptions', 'content')
    op.drop_column('job_descriptions', 'company')
    op.drop_column('job_descriptions', 'title')
