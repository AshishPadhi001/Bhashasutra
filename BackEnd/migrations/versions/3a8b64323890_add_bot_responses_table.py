"""Add bot_responses table

Revision ID: 3a8b64323890
Revises: 
Create Date: 2025-04-02 10:41:55.001917

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a8b64323890'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'bot_responses',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('question', sa.String(500), index=True, nullable=False),
        sa.Column('response', sa.Text, nullable=False),
        sa.Column('category', sa.String(100), index=True, nullable=True),
        sa.Column('is_faq', sa.Boolean, default=False, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
