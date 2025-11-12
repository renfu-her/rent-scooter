"""Add reservation status and expires_at to motorcycles

Revision ID: add_reservation_motorcycles
Revises: c78860628ed7
Create Date: 2025-01-XX XX:XX:XX.XXXXXX

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_reservation_motorcycles'
down_revision: Union[str, Sequence[str], None] = 'c78860628ed7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add reservation_expires_at column
    op.add_column('motorcycles', sa.Column('reservation_expires_at', sa.DateTime(), nullable=True))
    # Note: status column already exists, but we're updating the comment/documentation
    # The actual status values will be handled by the application code


def downgrade() -> None:
    """Downgrade schema."""
    # Remove reservation_expires_at column
    op.drop_column('motorcycles', 'reservation_expires_at')

