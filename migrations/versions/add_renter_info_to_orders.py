"""Add renter info to orders

Revision ID: add_renter_info_orders
Revises: add_reservations_table
Create Date: 2025-01-XX XX:XX:XX.XXXXXX

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_renter_info_orders'
down_revision: Union[str, Sequence[str], None] = 'add_reservations_table'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('orders', sa.Column('renter_name', sa.String(length=100), nullable=True))
    op.add_column('orders', sa.Column('renter_id_number', sa.String(length=20), nullable=True))
    op.add_column('orders', sa.Column('has_license', sa.Boolean(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('orders', 'has_license')
    op.drop_column('orders', 'renter_id_number')
    op.drop_column('orders', 'renter_name')

