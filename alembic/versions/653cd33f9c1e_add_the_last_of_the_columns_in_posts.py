"""add the last of the columns in posts

Revision ID: 653cd33f9c1e
Revises: ae78d3b62de0
Create Date: 2025-09-06 10:55:07.156572

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '653cd33f9c1e'
down_revision: Union[str, Sequence[str], None] = 'ae78d3b62de0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column(
        'published', 
        sa.Boolean(), 
        nullable=False, 
        server_default='TRUE'))
    op.add_column('posts',sa.Column(
        'created_at',
        sa.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
