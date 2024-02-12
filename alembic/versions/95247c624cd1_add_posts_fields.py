"""add posts fields

Revision ID: 95247c624cd1
Revises: d74baf7a4006
Create Date: 2024-02-12 16:16:09.372759

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95247c624cd1'
down_revision: Union[str, None] = 'd74baf7a4006'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', 
                  sa.Column('published', sa.Boolean, nullable=False, server_default='True')
                  ),
    op.add_column('posts',
                  sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
