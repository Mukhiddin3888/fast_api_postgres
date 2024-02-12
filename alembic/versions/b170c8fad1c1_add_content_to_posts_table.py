"""add content to posts table

Revision ID: b170c8fad1c1
Revises: 6e55d4f2f0ae
Create Date: 2024-02-12 15:36:16.838548

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b170c8fad1c1'
down_revision: Union[str, None] = '6e55d4f2f0ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String, nullable= False, default=''))
    
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
