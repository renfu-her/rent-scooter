"""Add reservations table

Revision ID: add_reservations_table
Revises: add_reservation_motorcycles
Create Date: 2025-01-XX XX:XX:XX.XXXXXX

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_reservations_table'
down_revision: Union[str, Sequence[str], None] = 'add_reservation_motorcycles'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('reservations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('motorcycle_id', sa.Integer(), nullable=False),
        sa.Column('renter_name', sa.String(length=100), nullable=False),
        sa.Column('renter_id_number', sa.String(length=20), nullable=False),
        sa.Column('has_license', sa.Boolean(), nullable=False),
        sa.Column('reservation_status', sa.String(length=20), nullable=False),
        sa.Column('reservation_expires_at', sa.DateTime(), nullable=True),
        sa.Column('contact_phone', sa.String(length=20), nullable=True),
        sa.Column('remarks', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['motorcycle_id'], ['motorcycles.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('reservations')

