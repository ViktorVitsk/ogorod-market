"""add timezone awareness to products.created_at

Revision ID: 8a5a2c90e4b0
Revises: da91b1363050
Create Date: 2025-03-09 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a5a2c90e4b0'
down_revision: Union[str, Sequence[str], None] = 'da91b1363050'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Make created_at timezone-aware."""
    op.alter_column(
        'products',
        'created_at',
        existing_type=sa.DateTime(),
        type_=sa.DateTime(timezone=True),
        existing_server_default=sa.text('CURRENT_TIMESTAMP'),
        server_default=sa.text('CURRENT_TIMESTAMP'),
        postgresql_using="created_at AT TIME ZONE 'UTC'",
        existing_nullable=True,
    )
    op.alter_column(
        'products',
        'created_at',
        nullable=False,
        existing_nullable=True,
    )


def downgrade() -> None:
    """Revert created_at to naive timestamps."""
    op.alter_column(
        'products',
        'created_at',
        nullable=True,
        existing_nullable=False,
    )
    op.alter_column(
        'products',
        'created_at',
        existing_type=sa.DateTime(timezone=True),
        type_=sa.DateTime(),
        existing_server_default=sa.text('CURRENT_TIMESTAMP'),
        server_default=sa.text('CURRENT_TIMESTAMP'),
        postgresql_using="created_at",
        existing_nullable=False,
    )
