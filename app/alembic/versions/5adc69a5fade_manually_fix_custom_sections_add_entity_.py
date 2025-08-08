"""manually fix custom_sections add entity_id and change user_id to profile_id

Revision ID: 5adc69a5fade
Revises: 839887842510
Create Date: 2025-08-08 17:12:11.178370

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5adc69a5fade'
down_revision: Union[str, Sequence[str], None] = '839887842510'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add entity_id column (UUID, unique, not null)
    op.add_column('custom_sections', sa.Column('entity_id', sa.UUID(), nullable=False, server_default=sa.text('gen_random_uuid()')))
    op.create_unique_constraint(None, 'custom_sections', ['entity_id'])
    
    # Add profile_id column
    op.add_column('custom_sections', sa.Column('profile_id', sa.Integer(), nullable=True))
    
    # Copy data from user_id to profile_id (since user_id was actually referencing profiles.id)
    op.execute('UPDATE custom_sections SET profile_id = user_id')
    
    # Make profile_id not nullable after data migration
    op.alter_column('custom_sections', 'profile_id', nullable=False)
    
    # Add foreign key constraint for profile_id
    op.create_foreign_key('custom_sections_profile_id_fkey', 'custom_sections', 'profiles', ['profile_id'], ['id'])
    
    # Drop the old user_id foreign key constraint and column
    op.drop_constraint('custom_sections_user_id_fkey', 'custom_sections', type_='foreignkey')
    op.drop_column('custom_sections', 'user_id')


def downgrade() -> None:
    """Downgrade schema."""
    # Add back user_id column
    op.add_column('custom_sections', sa.Column('user_id', sa.Integer(), nullable=True))
    
    # Copy data from profile_id to user_id
    op.execute('UPDATE custom_sections SET user_id = profile_id')
    
    # Make user_id not nullable
    op.alter_column('custom_sections', 'user_id', nullable=False)
    
    # Add back the foreign key constraint for user_id
    op.create_foreign_key('custom_sections_user_id_fkey', 'custom_sections', 'profiles', ['user_id'], ['id'])
    
    # Drop profile_id foreign key and column
    op.drop_constraint('custom_sections_profile_id_fkey', 'custom_sections', type_='foreignkey')
    op.drop_column('custom_sections', 'profile_id')
    
    # Drop entity_id constraint and column
    op.drop_constraint(None, 'custom_sections', type_='unique')
    op.drop_column('custom_sections', 'entity_id')
