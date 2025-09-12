"""add contect column

Revision ID: 4ccde9a8ea94
Revises: 2a5982a93d99
Create Date: 2025-09-06 09:56:27.267093

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ccde9a8ea94'
down_revision: Union[str, Sequence[str], None] = '2a5982a93d99'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass
