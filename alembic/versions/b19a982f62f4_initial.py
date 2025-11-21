"""initial

Revision ID: b19a982f62f4
Revises: 240db03b5d2d
Create Date: 2025-11-21 12:02:28.157561

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b19a982f62f4'
down_revision: Union[str, Sequence[str], None] = '240db03b5d2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # створюємо таблицю animals
    op.create_table(
        'animals',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('age', sa.Integer(), nullable=False),
        sa.Column('adopted', sa.Boolean(), nullable=False, default=False),
        sa.Column('health_status', sa.String(), nullable=True, default='healthy')
    )


def downgrade() -> None:
    """Downgrade schema."""
    # видаляємо таблицю animals
    op.drop_table('animals')
