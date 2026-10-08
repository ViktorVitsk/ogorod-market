"""unique cart item per product

Revision ID: c3e1a9d4b2f7
Revises: b1f8b3d8c9b5
Create Date: 2026-10-08 21:00:00.000000
"""

from typing import Sequence, Union

from alembic import op

revision: str = 'c3e1a9d4b2f7'
down_revision: Union[str, Sequence[str], None] = 'b1f8b3d8c9b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        'uq_cart_items_cart_id_product_id',
        'cart_items',
        ['cart_id', 'product_id'],
    )


def downgrade() -> None:
    op.drop_constraint(
        'uq_cart_items_cart_id_product_id',
        'cart_items',
        type_='unique',
    )
